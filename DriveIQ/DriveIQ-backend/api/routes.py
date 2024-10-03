import uuid
from flask import Blueprint, request, jsonify
from werkzeug.utils import secure_filename
import os
import random
from app.db import db, Driver, Trip, AggregatedData
from utils.jwt_auth import create_token, jwt_required
from utils.data_processing import process_gps_data
from utils.ml_integration import predict_driver_behavior
from datetime import datetime, timedelta
from sqlalchemy.exc import IntegrityError
import pandas as pd
from utils.mailer import send_otp_email
import json
from datetime import date
import logging

api_bp = Blueprint('api', __name__)

# Store OTPs temporarily (ideally, use Redis or a database)
otp_storage = {}

UPLOAD_FOLDER = 'uploads/identity_proofs'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Driver Registration Route with OTP Generation
@api_bp.route('/register', methods=['POST'])
def register():
    data = request.json
    name = data.get('name')
    email = data.get('email')
    password = data.get('password')
    accepted_terms = data.get('accepted_terms')

    if not name or not email or not password or not accepted_terms:
        logging.error("Missing registration data.")
        return jsonify({"error": "All fields are required"}), 400

    # Check if driver is already registered
    if Driver.query.filter_by(email=email).first():
        logging.error(f"Email {email} is already registered.")
        return jsonify({"error": "Email is already registered"}), 400

    # Generate OTP
    otp = random.randint(100000, 999999)
    otp_storage[email] = otp

    # Send OTP via email
    try:
        send_otp_email(email, otp)  # Use Nodemailer-like utility
        logging.info(f"OTP sent to {email} for registration.")
        return jsonify({"message": "OTP sent. Please verify your email."}), 200
    except Exception as e:
        logging.error(f"Failed to send OTP to {email}: {str(e)}")
        return jsonify({"error": "Failed to send OTP"}), 500

# OTP Verification Route
@api_bp.route('/verify-otp', methods=['POST'])
def verify_otp():
    data = request.json
    email = data.get('email')
    otp = data.get('otp')
    password = data.get('password')

    if otp_storage.get(email) == int(otp):
        driver = Driver.query.filter_by(email=email).first()

        if driver:
            return jsonify({"message": "User already exists."}), 400

        new_driver = Driver(name=data['name'], email=email, accepted_terms=True)
        new_driver.set_password(password)
        db.session.add(new_driver)
        db.session.commit()

        token = create_token(new_driver.id)
        return jsonify({"message": "OTP verified, registration successful", "token": token}), 200
    else:
        return jsonify({"error": "Invalid OTP"}), 400


# Define thresholds (SPEED_THRESHOLD for low speeds and STOP_TIME_THRESHOLD for idle time)
SPEED_THRESHOLD = 5  # m/s (~18 km/h)
STOP_TIME_THRESHOLD = timedelta(minutes=5)  # Idle time threshold before starting a new trip

def generate_unique_trip_id(driver_id):
    """Generate a truly unique trip ID."""
    return f'T-{driver_id}-{uuid.uuid4()}'

# Driver Login
@api_bp.route('/login', methods=['POST'])
def login():
    data = request.json
    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        logging.error("Missing email or password in login.")
        return jsonify({"error": "Email and password are required"}), 400

    driver = Driver.query.filter_by(email=email).first()
    if not driver or not driver.check_password(password):
        logging.error("Invalid login credentials.")
        return jsonify({"error": "Invalid credentials"}), 401

    token = create_token(driver.id)

    logging.info(f"Driver {email} logged in successfully.")
    return jsonify({"message": "Login successful", "token": token, "driver_id": driver.id}), 200

# Record GPS data and process trip
@api_bp.route('/record-telematics', methods=['POST'])
@jwt_required
def record_telematics():
    gps_data = request.json.get('gps_data', [])
    driver_id = request.json.get('driver_id')

    if not gps_data or not driver_id:
        logging.error("Invalid telematics data provided.")
        return jsonify({"error": "Invalid data provided"}), 400

    try:
        # Process the GPS data
        processed_data = process_gps_data(gps_data)

        # Check if a new trip should be started or continue the last trip
        latest_trip = Trip.query.filter_by(driver_id=driver_id).order_by(Trip.created_at.desc()).first()

        # Set flag for new trip
        start_new_trip = False

        if latest_trip:
            time_since_last_trip = (datetime.utcnow() - latest_trip.created_at).total_seconds()
            if processed_data['avg_speed'] < SPEED_THRESHOLD and time_since_last_trip > STOP_TIME_THRESHOLD.total_seconds():
                start_new_trip = True
        else:
            start_new_trip = True

        trip_id = generate_unique_trip_id(driver_id) if start_new_trip else latest_trip.trip_id

        # Prepare data for ML model prediction
        ml_ready_data = {
            'Speed(m/s)': processed_data['avg_speed'],
            'Acceleration(m/s^2)': processed_data['avg_acceleration'],
            'Heading_Change(degrees)': processed_data['avg_heading_change'],
            'Jerk(m/s^3)': processed_data['avg_jerk'],
            'Braking_Intensity': processed_data['avg_braking_intensity'],
            'SASV': processed_data['avg_sasv'],
            'Speed_Violation': processed_data.get('Speed_Violation', 0)
        }

        score, category = predict_driver_behavior(pd.DataFrame([ml_ready_data]))

        new_trip = Trip(
            driver_id=driver_id,
            trip_id=trip_id,
            gps_data=json.dumps(gps_data),
            avg_speed=processed_data['avg_speed'],
            avg_acceleration=processed_data['avg_acceleration'],
            avg_jerk=processed_data['avg_jerk'],
            avg_heading_change=processed_data['avg_heading_change'],
            avg_braking_intensity=processed_data['avg_braking_intensity'],
            avg_sasv=processed_data['avg_sasv'],
            total_distance=processed_data['total_distance'],
            score=score,
            category=category,
            created_at=datetime.utcnow()
        )

        db.session.add(new_trip)
        db.session.commit()

        logging.info(f"Telematics data recorded for driver {driver_id}, trip {trip_id}.")
        return jsonify({
            "message": "Telematics data recorded",
            "trip_id": trip_id,
            "driving_score": score,
            "driving_category": category
        }), 200

    except IntegrityError:
        db.session.rollback()
        trip_id = generate_unique_trip_id(driver_id)
        new_trip.trip_id = trip_id
        db.session.add(new_trip)
        db.session.commit()

        logging.info(f"Telematics data recorded after resolving ID conflict for trip {trip_id}.")
        return jsonify({
            "message": "Telematics data recorded after resolving ID conflict",
            "trip_id": trip_id,
            "driving_score": score,
            "driving_category": category
        }), 200

    except Exception as e:
        logging.error(f"Error processing telematics data: {str(e)}")
        return jsonify({"error": f"Error processing data: {str(e)}"}), 500


@api_bp.route('/process-daily-data', methods=['POST'])
@jwt_required
def process_daily_data():
    driver_id = request.json.get('driver_id')

    if not driver_id:
        logging.error("Driver ID is required for daily data processing.")
        return jsonify({"error": "Driver ID is required"}), 400

    driver = Driver.query.get(driver_id)
    if not driver:
        logging.error(f"Driver {driver_id} not found for daily data processing.")
        return jsonify({"error": "Driver not found"}), 404

    last_24_hours = datetime.utcnow() - timedelta(days=1)
    trips = Trip.query.filter(Trip.driver_id == driver_id, Trip.created_at >= last_24_hours).all()

    if not trips:
        logging.error(f"No trips found for driver {driver_id} to calculate daily metrics.")
        return jsonify({"error": "No trips found to calculate daily metrics"}), 404

    # Initialize total metrics for aggregation
    total_distance, total_speed_kmph, total_speed_mps = 0, 0, 0
    total_acceleration, total_jerk = 0, 0
    total_heading_change, total_braking_intensity, total_sasv, total_speed_violation = 0, 0, 0, 0
    total_entries = 0

    for trip in trips:
        try:
            gps_data = json.loads(trip.gps_data)
            processed_data = process_gps_data(gps_data)

            # Ensure all required keys are present
            processed_data.setdefault('SASV', 0)  # Default SASV to 0 if not present
            processed_data.setdefault('Speed_Violation', 0)  # Default Speed Violation to 0 if not present

            # Aggregate metrics from each trip
            total_distance += processed_data['total_distance']
            total_speed_kmph += processed_data['avg_speed_kmph']  # Speed in km/h for display
            total_speed_mps += processed_data['avg_speed_mps']  # Speed in m/s for prediction
            total_acceleration += processed_data['avg_acceleration']
            total_jerk += processed_data['avg_jerk']
            total_heading_change += processed_data['avg_heading_change']
            total_braking_intensity += processed_data['avg_braking_intensity']
            total_sasv += processed_data['SASV']
            total_speed_violation += processed_data['Speed_Violation']
            total_entries += 1

        except ValueError as e:
            logging.error(f"Error processing trip {trip.trip_id}: {str(e)}")
            continue

    if total_entries > 0:
        # Calculate average metrics over all trips
        avg_speed_kmph = total_speed_kmph / total_entries
        avg_speed_mps = total_speed_mps / total_entries
        avg_acceleration = total_acceleration / total_entries
        avg_jerk = total_jerk / total_entries
        avg_heading_change = total_heading_change / total_entries
        avg_braking_intensity = total_braking_intensity / total_entries
        avg_sasv = total_sasv / total_entries
        avg_speed_violation = total_speed_violation / total_entries

        aggregated_data = {
            'Speed(km/h)': avg_speed_kmph,
            'Speed(m/s)': avg_speed_mps,
            'Acceleration(m/s^2)': avg_acceleration,
            'Heading_Change(degrees)': avg_heading_change,
            'Jerk(m/s^3)': avg_jerk,
            'Braking_Intensity': avg_braking_intensity,
            'SASV': avg_sasv,  # Ensure this field is passed
            'Speed_Violation': avg_speed_violation  # Ensure this field is passed
        }

        # Call the ML model to predict driving score and category
        driving_score, driving_category = predict_driver_behavior(pd.DataFrame([aggregated_data]))

        # Save the aggregated data in the database with driving score and category
        aggregated_entry = AggregatedData(
            driver_id=driver_id,
            period="daily",
            date=date.today(),  # Store the current day’s data
            avg_speed=avg_speed_mps,
            avg_acceleration=avg_acceleration,
            avg_jerk=avg_jerk,
            avg_heading_change=avg_heading_change,
            avg_braking_intensity=avg_braking_intensity,
            avg_sasv=avg_sasv,
            speed_violation_count=avg_speed_violation,
            total_observations=total_entries,
            driving_score=driving_score,  # Save driving score
            driving_category=driving_category,  # Save driving category
            created_at=datetime.utcnow()
        )

        db.session.add(aggregated_entry)
        db.session.commit()

        logging.info(f"Daily data processed for driver {driver_id}.")
        return jsonify({
            "message": "Daily data processed successfully",
            "driving_score": driving_score,
            "driving_category": driving_category,
            "aggregated_data": aggregated_data,
            "total_trips": len(trips),
            "total_distance_covered_km": total_distance / 1000
        }), 200

    logging.error(f"No valid trips found for driver {driver_id} to calculate daily metrics.")
    return jsonify({"error": "No valid trips found to calculate daily metrics"}), 400
