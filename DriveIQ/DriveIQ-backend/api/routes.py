from flask import Blueprint, request, jsonify
from utils.data_processing import process_gps_data, fetch_sensitive_areas
from utils.ml_integration import predict_driver_behavior
import numpy as np

# Define the Blueprint
api_bp = Blueprint('api', __name__)

@api_bp.route('/start-journey', methods=['POST'])
def start_journey():
    data = request.json
    trip_id = 1  # Mock trip_id, replace with actual DB call
    return jsonify({"message": "Journey started", "trip_id": trip_id}), 201

@api_bp.route('/record-telematics', methods=['POST'])
def record_telematics():
    gps_data = request.json.get('gps_data', [])

    if not gps_data:
        return jsonify({"error": "No GPS data provided"}), 400

    # Process the GPS data to calculate speed, acceleration, etc.
    try:
        first_point = gps_data[0] if gps_data else None
        sensitive_areas = []
        if first_point:
            # Fetch sensitive areas around the first GPS point
            sensitive_areas = fetch_sensitive_areas(first_point['Latitude'], first_point['Longitude'])
        
        processed_data = process_gps_data(gps_data)
    except Exception as e:
        return jsonify({"error": f"Error processing GPS data: {str(e)}"}), 500

    # Send processed data to the ML model for prediction
    try:
        score, category, penalties = predict_driver_behavior(processed_data)
    except Exception as e:
        return jsonify({"error": f"Error predicting driver behavior: {str(e)}"}), 500

    # Ensure score is converted to Python int or float for JSON serialization
    score = int(score) if isinstance(score, np.integer) else float(score)

    # If driving behavior is risky, return the penalty breakdown
    if category == 'Risky':
        return jsonify({
            "driving_score": score,
            "driving_category": category,
            "penalty_breakdown": penalties
        }), 200

    return jsonify({
        "driving_score": score,
        "driving_category": category
    }), 200

@api_bp.route('/history/<int:user_id>', methods=['GET'])
def get_history(user_id):
    # Mock history data, replace with actual DB calls
    mock_history = [
        {"trip_id": 1, "driving_score": 85, "category": "Safe"},
        {"trip_id": 2, "driving_score": 72, "category": "Moderate"}
    ]
    return jsonify(mock_history), 200
