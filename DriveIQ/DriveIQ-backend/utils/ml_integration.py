# ml_integration.py
import os
import numpy as np
import pickle
import pandas as pd

# Paths to the trip-level and bulk-level model files and scalers
current_dir = os.path.dirname(os.path.abspath(__file__))

# Trip-level model and scaler
trip_model_path = os.path.join(current_dir, '../../ml_model/models/driving_data_model.pkl')
trip_scaler_path = os.path.join(current_dir, '../../ml_model/models/scaler.pkl')

# Bulk-level model and scaler
bulk_model_path = os.path.join(current_dir, '../../ml_model/models/bulk_driving_model.pkl')
bulk_scaler_path = os.path.join(current_dir, '../../ml_model/models/bulk_scaler.pkl')

# Load the trip-level model and scaler
with open(trip_model_path, 'rb') as trip_model_file:
    trip_model = pickle.load(trip_model_file)
with open(trip_scaler_path, 'rb') as trip_scaler_file:
    trip_scaler = pickle.load(trip_scaler_file)

# Load the bulk-level model and scaler
with open(bulk_model_path, 'rb') as bulk_model_file:
    bulk_model = pickle.load(bulk_model_file)
with open(bulk_scaler_path, 'rb') as bulk_scaler_file:
    bulk_scaler = pickle.load(bulk_scaler_file)

# Categorize driving score based on thresholds
def categorize_driving_score(score):
    if score >= 85:
        return 'Safe'
    elif score >= 60:
        return 'Moderate'
    else:
        return 'Risky'

# Function to calculate driving score from category probabilities
def calculate_driving_score_from_probabilities(category_probabilities):
    weighted_scores = np.dot(category_probabilities, [20, 50, 100])
    return np.mean(weighted_scores)

# Function to predict driving behavior for a single trip
def predict_driver_behavior(processed_data):
    features = ['Speed(m/s)', 'Acceleration(m/s^2)', 'Heading_Change(degrees)', 'Jerk(m/s^3)', 'Braking_Intensity', 'SASV', 'Speed_Violation']

    if any(f not in processed_data.columns for f in features):
        raise ValueError(f"Missing required features for prediction: {', '.join(features)}")

    # Scale the data for trip-level prediction
    processed_data_scaled = trip_scaler.transform(processed_data[features])

    # Predict category probabilities using the trip-level model
    category_probabilities = trip_model.predict_proba(processed_data_scaled)

    # Calculate the driving score
    driving_score = calculate_driving_score_from_probabilities(category_probabilities)

    # Categorize the driving behavior
    driving_category = categorize_driving_score(driving_score)

    return int(driving_score), driving_category

# Function to predict consolidated driving score based on bulk data (aggregated from multiple trips)
def predict_bulk_driver_behavior(bulk_features):
    feature_columns = [
        'Speed(m/s)_mean', 'Speed(m/s)_max', 'Speed(m/s)_std',
        'Acceleration(m/s^2)_mean', 'Acceleration(m/s^2)_max', 'Acceleration(m/s^2)_std',
        'Heading_Change(degrees)_mean', 'Jerk(m/s^3)_mean',
        'Braking_Intensity_mean', 'SASV_mean', 'Speed_Violation_mean', 'Total_Observations'
    ]

    # Ensure all required features are present
    for feature in feature_columns:
        if feature not in bulk_features:
            raise ValueError(f"Missing required feature: {feature}")

    # Create DataFrame for bulk features and scale the data
    bulk_data = pd.DataFrame([bulk_features])
    bulk_data_scaled = bulk_scaler.transform(bulk_data[feature_columns])

    # Predict category using the bulk-level model
    predicted_category = bulk_model.predict(bulk_data_scaled)

    return categorize_driving_score(predicted_category[0])
