from flask import Blueprint, request, jsonify
from flask_socketio import emit
from utils.data_processing import process_gps_data
from utils.ml_integration import predict_driver_behavior
from app.db import db, Driver, Trip
import time
import pandas as pd

api_bp = Blueprint('api', __name__)

# Register a new user
@api_bp.route('/register', methods=['POST'])
def register():
    data = request.json
    driver_name = data.get('name')
    accepted_terms = data.get('accepted_terms')

    if not driver_name:
        return jsonify({"error": "Driver name is required"}), 400
    if not accepted_terms:
        return jsonify({"error": "You must accept the terms and conditions"}), 400

    existing_driver = Driver.query.filter_by(name=driver_name).first()
    if existing_driver:
        return jsonify({"error": "Driver already registered"}), 400

    new_driver = Driver(name=driver_name)
    db.session.add(new_driver)
    db.session.commit()

    return jsonify({"message": "Registration successful", "driver_id": new_driver.id}), 201

# Login user
@api_bp.route('/login', methods=['POST'])
def login():
    data = request.json
    driver_name = data.get('name')

    if not driver_name:
        return jsonify({"error": "Driver name is required"}), 400

    driver = Driver.query.filter_by(name=driver_name).first()
    if not driver:
        return jsonify({"error": "No account found. Please register."}), 404

    return jsonify({"message": "Login successful", "driver_id": driver.id}), 200

# Start a new journey (no need for driver_name every time)
@api_bp.route('/start-journey', methods=['POST'])
def start_journey():
    data = request.json
    driver_id = data.get('driver_id')

    driver = Driver.query.get(driver_id)
    if not driver:
        return jsonify({"error": "Driver not found"}), 404

    latest_trip = Trip.query.filter_by(driver_id=driver.id).order_by(Trip.id.desc()).first()
    next_trip_id = f'T-{int(latest_trip.trip_id.split("-")[1]) + 1}' if latest_trip else 'T-1'

    return jsonify({
        "message": "Journey started",
        "driver_id": driver.id,
        "trip_id": next_trip_id
    }), 201

# Record telematics data
@api_bp.route('/record-telematics', methods=['POST'])
def record_telematics():
    gps_data = request.json.get('gps_data', [])
    driver_id = request.json.get('driver_id')
    trip_id = request.json.get('trip_id')

    if not gps_data or not driver_id or not trip_id:
        return jsonify({"error": "Invalid data provided"}), 400

    try:
        processed_data = process_gps_data(gps_data)
        score, category = predict_driver_behavior(processed_data)

        new_trip = Trip(
            driver_id=driver_id,
            trip_id=trip_id,
            gps_data=str(gps_data),
            score=score,
            category=category,
            created_at=pd.Timestamp.utcnow()
        )
        db.session.add(new_trip)
        db.session.commit()

        return jsonify({
            "driving_score": score,
            "driving_category": category
        }), 200

    except Exception as e:
        return jsonify({"error": f"Error processing data: {str(e)}"}), 500


# WebSocket: Real-time data streaming for drivers
@api_bp.route('/stream-telematics', methods=['POST'])
def stream_telematics():
    gps_data = request.json.get('gps_data', [])
    driver_id = request.json.get('driver_id')

    if not gps_data or not driver_id:
        return jsonify({"error": "Invalid data provided"}), 400

    try:
        while True:
            processed_data = process_gps_data(gps_data)
            emit('gps_update', processed_data, namespace='/driver')
            time.sleep(2)

    except Exception as e:
        return jsonify({"error": f"Error streaming data: {str(e)}"}), 500
