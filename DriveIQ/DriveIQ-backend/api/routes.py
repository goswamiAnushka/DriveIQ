from flask import request, jsonify
from utils.data_processing import preprocess_gps_data
from utils.ml_integration import load_model, predict_driver_behavior
from . import api_bp

@api_bp.route('/start-journey', methods=['POST'])
def start_journey():
    return jsonify({"message": "Journey started, collecting GPS data."})

@api_bp.route('/record-telematics', methods=['POST'])
def record_telematics():
    gps_data = request.json.get('gps_data')
    if not gps_data:
        return jsonify({"error": "No GPS data provided"}), 400

    # Preprocess GPS data to extract features
    processed_data = preprocess_gps_data(gps_data)
    
    # Predict driving behavior and score
    model = load_model()
    prediction = predict_driver_behavior(model, processed_data)
    
    return jsonify(prediction)
