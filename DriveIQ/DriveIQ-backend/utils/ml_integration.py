import os
import numpy as np
import pickle
from sklearn.preprocessing import StandardScaler
import pandas as pd

# Corrected paths to the model and scaler files
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

# Function to predict driving score and category using the trained model
def predict_driver_behavior(processed_data):
    """
    Predict the driving behavior and score using the ML model.
    
    Parameters:
    processed_data (pd.DataFrame): A DataFrame containing the processed telematics data.
    
    Returns:
    driving_score (int): The calculated driving score out of 100.
    driving_category (str): The predicted driving category (e.g., Risky, Moderate, Good, Excellent).
    """
    # Ensure the necessary features are available in the processed data
    features = ['Speed(m/s)', 'Acceleration(m/s^2)', 'Heading_Change(degrees)', 'Jerk(m/s^3)', 'Braking_Intensity']
    
    # Convert processed_data to a DataFrame if it is a list
    if isinstance(processed_data, list):
        processed_data = pd.DataFrame(processed_data)

    # Check if all required columns are in the DataFrame
    missing_features = [f for f in features if f not in processed_data.columns]
    if missing_features:
        raise ValueError(f"Missing required features for prediction: {', '.join(missing_features)}")

    # Extract only the necessary features for prediction
    processed_data = processed_data[features]

    # Scale the features using the pre-trained scaler
    scaled_data = scaler.transform(processed_data)

    # Predict category probabilities and the predicted class for each sample
    category_probabilities = model.predict_proba(scaled_data)
    category_pred = model.predict(scaled_data)

    # Map numeric category predictions to readable labels
    category_mapping = {0: 'Risky', 1: 'Moderate', 2: 'Good', 3: 'Excellent'}
    driving_category = category_mapping.get(np.argmax(np.bincount(category_pred)), 'Unknown')

    # Calculate the weighted driving score out of 100
    driving_score = np.mean([np.dot(probs, [20, 50, 75, 100]) for probs in category_probabilities])

    return int(driving_score), driving_category
