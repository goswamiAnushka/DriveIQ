from flask import request, jsonify
from utils.data_processing import preprocess_gps_data
from utils.ml_integration import load_model, predict_driver_behavior
from utils.history_management import save_journey, get_journey_history
from utils.suggestions import generate_suggestions
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
    
    # Save journey history
    save_journey(prediction)
    
    # Generate suggestions based on prediction
    suggestions = generate_suggestions(prediction)
    
    response = {
        "prediction": prediction,
        "suggestions": suggestions
    }
    
    return jsonify(response)

@api_bp.route('/history', methods=['GET'])
def history():
    # Retrieve journey history
    journey_history = get_journey_history()
    return jsonify(journey_history)
