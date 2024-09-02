from flask import Blueprint, request, jsonify
from utils.data_processing import preprocess_data, calculate_features  # Ensure these functions exist
from utils.ml_integration import load_model, predict_behavior

api = Blueprint('api', __name__)

@api.route('/health', methods=['GET'])
def health_check():
    """Health check route to ensure the API is running."""
    return jsonify({"status": "healthy"}), 200

@api.route('/predict', methods=['POST'])
def predict():
    """API route to predict driving behavior based on GPS data."""
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "No input data provided"}), 400

        # Extract GPS points and timestamps from input
        gps_data = data.get('gps_data')
        if not gps_data or not isinstance(gps_data, list):
            return jsonify({"error": "Invalid GPS data format"}), 400

        # Calculate speed, acceleration, and heading change
        processed_data = calculate_features(gps_data)

        # Preprocess the data
        processed_data = preprocess_data(processed_data)

        # Load the model
        model = load_model()

        # Predict behavior
        prediction = predict_behavior(model, processed_data)

        return jsonify({"prediction": prediction}), 200

    except KeyError as e:
        return jsonify({"error": f"Missing key in input data: {str(e)}"}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500
