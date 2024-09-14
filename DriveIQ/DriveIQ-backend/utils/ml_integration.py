import os
import numpy as np
import pickle
from sklearn.preprocessing import StandardScaler
import pandas as pd

# Paths to the model and scaler files
current_dir = os.path.dirname(os.path.abspath(__file__))
model_path = os.path.join(current_dir, '../../ml_model/models/driving_data_model.pkl')
scaler_path = os.path.join(current_dir, '../../ml_model/models/scaler.pkl')

# Ensure the model file exists
if not os.path.exists(model_path):
    raise FileNotFoundError(f"Model file not found at {model_path}. Ensure the model is trained and saved correctly.")

# Load the trained model
with open(model_path, 'rb') as model_file:
    model = pickle.load(model_file)

# Ensure the scaler file exists
if not os.path.exists(scaler_path):
    raise FileNotFoundError(f"Scaler file not found at {scaler_path}. Ensure the scaler is trained and saved correctly.")

# Load the scaler
with open(scaler_path, 'rb') as scaler_file:
    scaler = pickle.load(scaler_file)

# Function to categorize driving based on the score
def categorize_driving_score(score):
    if score >= 85:
        return 'Safe'
    elif score >= 60:
        return 'Moderate'
    else:
        return 'Risky'

# Function to calculate driving score from category probabilities
def calculate_driving_score_from_probabilities(category_probabilities):
    """
    Calculate a weighted driving score from the category probabilities.
    Category weights: Risky = 20, Moderate = 50, Safe = 100
    """
    weighted_scores = np.dot(category_probabilities, [20, 50, 100])
    return np.mean(weighted_scores)

# Function to calculate penalties for risky driving behavior
def calculate_penalties(processed_data):
    penalties = {
        "speed_penalty": int(processed_data['Speed(m/s)'].mean() * 2),  # Example: multiply by a factor
        "acceleration_penalty": int(processed_data['Acceleration(m/s^2)'].mean() * 5),
        "heading_change_penalty": int(processed_data['Heading_Change(degrees)'].mean() * 3),
        "sensitive_area_violation_penalty": int(processed_data['SASV'].sum() * 10),
        "speed_violation_penalty": int(processed_data['Speed_Violation'].sum() * 15)
    }
    return penalties

# Function to predict driving score and category using the trained model
def predict_driver_behavior(processed_data):
    """
    Predict the driving behavior and score using the ML model.
    
    Parameters:
    processed_data (pd.DataFrame): A DataFrame containing the processed telematics data.
    
    Returns:
    driving_score (int): The calculated driving score out of 100.
    driving_category (str): The predicted driving category (e.g., Risky, Moderate, Safe).
    penalties (dict): Penalty breakdown if driving is risky.
    """
    features = ['Speed(m/s)', 'Acceleration(m/s^2)', 'Heading_Change(degrees)', 'Jerk(m/s^3)', 'Braking_Intensity', 'SASV', 'Speed_Violation']

    missing_features = [f for f in features if f not in processed_data.columns]
    if missing_features:
        raise ValueError(f"Missing required features for prediction: {', '.join(missing_features)}")

    # Extract necessary features
    processed_data = processed_data[features]
    scaled_data = scaler.transform(processed_data)

    # Predict category probabilities
    category_probabilities = model.predict_proba(scaled_data)

    # Calculate driving score
    driving_score = calculate_driving_score_from_probabilities(category_probabilities)

    # Categorize driving behavior
    driving_category = categorize_driving_score(driving_score)

    # If the category is 'Risky', calculate penalties
    if driving_category == 'Risky':
        penalties = calculate_penalties(processed_data)
        return int(driving_score), driving_category, penalties

    return int(driving_score), driving_category, None
