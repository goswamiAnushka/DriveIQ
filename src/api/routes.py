# src/api/routes.py
from flask import Blueprint, request, jsonify
from ..utils import load_model, preprocess_input

api_routes = Blueprint('api_routes', __name__)

model = load_model()

@api_routes.route('/predict', methods=['POST'])
def predict():
    if request.method == 'POST':
        try:
            data = request.json
            preprocessed_data = preprocess_input(data)
            prediction = model.predict(preprocessed_data)
            behavior_mapping = {0: 'Safe', 1: 'Moderate', 2: 'Average', 3: 'Aggressive'}
            predicted_behavior = behavior_mapping[prediction[0]]
            return jsonify({'status': 'success', 'predicted_behavior': predicted_behavior}), 200
        except Exception as e:
            return jsonify({'status': 'error', 'message': str(e)}), 400
