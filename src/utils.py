# src/utils.py
import pickle
import pandas as pd
from sklearn.preprocessing import StandardScaler

def load_model():
    """Load the trained machine learning model from disk."""
    with open('../models/driving_behavior_model.pkl', 'rb') as model_file:
        model = pickle.load(model_file)
    return model

def preprocess_input(data):
    """Preprocess the input data for the model."""
    # Assuming the data comes as a dictionary from the POST request
    df = pd.DataFrame([data])
    
    # Perform the same feature engineering as in the training phase
    scaler = StandardScaler()
    scaled_features = scaler.fit_transform(df[['avg_speed', 'max_acceleration', 'total_heading_change']])
    
    return scaled_features
