from flask import Blueprint, request, jsonify
import pickle
import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler

# Load the model and scaler
model = pickle.load(open('../models/driving_behavior_model.pkl', 'rb'))
scaler = pickle.load(open('../models/scaler.pkl', 'rb'))

api_bp = Blueprint('api_bp', __name__)

@api_bp.route('/predict', methods=['POST'])
def predict_behavior():
    data = request.json
    # Assuming data contains 'avg_speed', 'max_acceleration', 'total_heading_change'
    features = np.array([[data['avg_speed'], data['max_acceleration'], data['total_heading_change']]])
    
    # Scale features
    scaled_features = scaler.transform(features)
    
    # Predict behavior
    prediction = model.predict(scaled_features)
    behavior_mapping = {0: 'Safe', 1: 'Moderate', 2: 'Average', 3: 'Aggressive'}
    behavior = behavior_mapping[prediction[0]]
    
    return jsonify({'predicted_behavior': behavior})

# Optional retraining endpoint
@api_bp.route('/train', methods=['POST'])
def retrain_model():
    # Logic for retraining the model with new data
    return jsonify({'message': 'Model retrained successfully!'})
