from flask import Blueprint, request, jsonify
from utils.data_processing import process_gps_data
from utils.ml_integration import predict_driver_behavior
from app.db import db, Driver, Trip
import pandas as pd

api_bp = Blueprint('api', __name__)

# Start a new journey
@api_bp.route('/start-journey', methods=['POST'])
def start_journey():
    data = request.json
    driver_name = data.get('name', None)

    if driver_name is None:
        return jsonify({"error": "Driver name is required"}), 400

    # Check if the driver exists or create a new one
    driver = Driver.query.filter_by(name=driver_name).first()
    if not driver:
        driver = Driver(name=driver_name)
        db.session.add(driver)
        db.session.commit()

    # Generate the next trip ID
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

    if not gps_data or not driver_id:
        return jsonify({"error": "Invalid data provided"}), 400

    try:
        # Generate the next trip ID
        latest_trip = Trip.query.filter_by(driver_id=driver_id).order_by(Trip.id.desc()).first()
        next_trip_id = f'T-{int(latest_trip.trip_id.split("-")[1]) + 1}' if latest_trip else 'T-1'

        # Process GPS data
        processed_data = process_gps_data(gps_data)

        # Predict driving behavior
        score, category = predict_driver_behavior(processed_data)

        # Save trip data in SQLite
        new_trip = Trip(
            driver_id=driver_id,
            trip_id=next_trip_id,
            gps_data=str(gps_data),
            score=score,
            category=category,
            created_at=pd.Timestamp.utcnow()
        )
        db.session.add(new_trip)
        db.session.commit()

        return jsonify({
            "driving_score": score,
            "driving_category": category,
            "trip_id": next_trip_id
        }), 200

    except Exception as e:
        return jsonify({"error": f"Error processing data: {str(e)}"}), 500
