import pandas as pd
import numpy as np
import os
from math import radians, sin, cos, sqrt, atan2

def ensure_directory_exists(directory):
    """Create directory if it does not exist."""
    if not os.path.exists(directory):
        os.makedirs(directory)

def haversine(lat1, lon1, lat2, lon2):
    """Calculate the great-circle distance between two points on the Earth's surface."""
    R = 6371e3  # Earth radius in meters
    phi1 = np.radians(lat1)
    phi2 = np.radians(lat2)
    delta_phi = np.radians(lat2 - lat1)
    delta_lambda = np.radians(lon2 - lon1)
    
    a = np.sin(delta_phi / 2.0)**2 + np.cos(phi1) * np.cos(phi2) * np.sin(delta_lambda / 2.0)**2
    c = 2 * np.arctan2(np.sqrt(a), np.sqrt(1 - a))
    
    return R * c  # Distance in meters

def calculate_features(gps_data):
    df = pd.DataFrame(gps_data)
    
    # Rename columns to match expected names in preprocessing functions
    df.rename(columns={
        'latitude': 'Latitude',
        'longitude': 'Longitude',
        'timestamp': 'Time_Step'
    }, inplace=True)
    
    # Calculate speed, acceleration, heading change, and jerk
    df = calculate_speed(df)
    df = calculate_acceleration(df)
    df = calculate_heading_change(df)
    df = calculate_jerk(df)

    return df


# Use the functions as needed
def calculate_speed(df):
    """Calculate speed using Haversine formula between consecutive points."""
    df['Distance(m)'] = np.sqrt(
        np.diff(df['Latitude'], prepend=df['Latitude'][0])**2 +
        np.diff(df['Longitude'], prepend=df['Longitude'][0])**2
    ) * 111320  # Approximation: 1 degree latitude ≈ 111.32 km
    
    df['Speed(m/s)'] = df['Distance(m)'] / df['Time_Step'].diff().fillna(1)
    return df

def calculate_acceleration(df):
    """Calculate acceleration as the rate of change of speed."""
    df['Acceleration(m/s^2)'] = df['Speed(m/s)'].diff().fillna(0)
    return df

def calculate_heading_change(df):
    """Calculate heading change based on bearing between two points."""
    lat1 = np.radians(df['Latitude'].shift())
    lon1 = np.radians(df['Longitude'].shift())
    lat2 = np.radians(df['Latitude'])
    lon2 = np.radians(df['Longitude'])
    
    delta_lon = lon2 - lon1
    x = np.sin(delta_lon) * np.cos(lat2)
    y = np.cos(lat1) * np.sin(lat2) - np.sin(lat1) * np.cos(lat2) * np.cos(delta_lon)
    df['Heading_Change(degrees)'] = np.degrees(np.arctan2(x, y))
    
    return df

def calculate_jerk(df):
    """Calculate jerk as the rate of change of acceleration."""
    df['Jerk(m/s^3)'] = df['Acceleration(m/s^2)'].diff().fillna(0)
    return df

def preprocess_data(df):
    """Preprocess the data if needed before feeding into the model."""
    # Perform preprocessing steps here
    # This can be more comprehensive, depending on your specific needs.
    return df
