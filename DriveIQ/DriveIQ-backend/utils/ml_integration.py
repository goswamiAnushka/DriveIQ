import os
import numpy as np
import pickle
import pandas as pd
import logging
from scipy import stats


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
    if score >= 80:
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
    if not isinstance(processed_data, pd.DataFrame):
        raise ValueError("Input data must be a pandas DataFrame")

    # Features required for the ML model
    features = ['Speed(m/s)', 'Acceleration(m/s^2)', 'Heading_Change(degrees)', 
                'Jerk(m/s^3)', 'Braking_Intensity', 'SASV', 'Speed_Violation']

    # Ensure all required columns are present
    missing_features = [f for f in features if f not in processed_data.columns]
    if missing_features:
        raise ValueError(f"Missing required features for prediction: {', '.join(missing_features)}")

    # Scale the data and predict category probabilities
    processed_data_scaled = trip_scaler.transform(processed_data[features])
    category_probabilities = trip_model.predict_proba(processed_data_scaled)

    # Calculate driving score and category
    driving_score = calculate_driving_score_from_probabilities(category_probabilities)
    driving_category = categorize_driving_score(driving_score)

    return int(driving_score), driving_category

# Function to predict bulk driving behavior using aggregated data
def predict_bulk_driver_behavior(bulk_data):
    # Ensure feature consistency in the bulk model
    feature_columns = [
        'Speed(m/s)_mean', 'Acceleration(m/s^2)_mean', 'Heading_Change(degrees)_mean',
        'Jerk(m/s^3)_mean', 'Braking_Intensity_mean', 'SASV_total', 'Speed_Violation_total'
    ]

    try:
        # Convert bulk_data to DataFrame
        bulk_data_df = pd.DataFrame(bulk_data)

        # Ensure all required columns are present
        missing_features = [f for f in feature_columns if f not in bulk_data_df.columns]
        if missing_features:
            raise ValueError(f"Missing required features for prediction: {', '.join(missing_features)}")

        # Scale the data for prediction
        bulk_data_scaled = bulk_scaler.transform(bulk_data_df[feature_columns])

        # Predict category probabilities using the bulk model
        category_probabilities = bulk_model.predict_proba(bulk_data_scaled)

        # Calculate the average score and determine the most frequent category
        average_score = calculate_driving_score_from_probabilities(category_probabilities)
        driving_category = categorize_driving_score(average_score)

        return driving_category, int(average_score)

    except Exception as e:
        logging.error(f"Error during bulk prediction: {str(e)}")
        raise
