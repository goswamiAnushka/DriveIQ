# src/api/routes.py
from flask import Blueprint, request, jsonify
from src.utils import load_model, preprocess_input

# Create a blueprint for the API routes
api_routes = Blueprint('api_routes', __name__)

# Load the model once at the start
model = load_model()

@api_routes.route('/predict', methods=['POST'])
def predict():
    """Endpoint to handle predictions based on user input."""
    if request.method == 'POST':
        try:
            # Get data from the request
            data = request.json
            
            # Preprocess the input
            preprocessed_data = preprocess_input(data)
            
            # Make prediction
            prediction = model.predict(preprocessed_data)
            
            # Map numeric predictions back to behavior categories
            behavior_mapping = {0: 'Safe', 1: 'Moderate', 2: 'Average', 3: 'Aggressive'}
            predicted_behavior = behavior_mapping[prediction[0]]
            
            # Return the prediction result as JSON
            return jsonify({
                'status': 'success',
                'predicted_behavior': predicted_behavior
            }), 200
        
        except Exception as e:
            return jsonify({
                'status': 'error',
                'message': str(e)
            }), 400
