import pickle
import numpy as np

def load_model():
    with open('DriveIQ-backend/models/driving_behavior_model.pkl', 'rb') as model_file:
        model = pickle.load(model_file)
    return model

def predict_driver_behavior(model, features):
    # Convert features to numpy array for model prediction
    features_array = features[['Speed(m/s)', 'Acceleration(m/s^2)', 'Heading_Change(degrees)', 'Jerk(m/s^3)']].values
    prediction = model.predict(features_array)
    score = np.mean(features['Driving_Score'])  # Calculate the mean driving score for the trip
    behavior = features['Driving_Category'].mode()[0]  # Most frequent driving category for the trip
    return {"behavior": behavior, "score": score}
