import pandas as pd
import numpy as np
from math import radians, cos, sin, sqrt, atan2, degrees

# Haversine formula to calculate distance between two points
def haversine(lat1, lon1, lat2, lon2):
    R = 6371  # Radius of the Earth in km
    d_lat = radians(lat2 - lat1)
    d_lon = radians(lat2 - lon1)
    a = sin(d_lat/2) ** 2 + cos(radians(lat1)) * cos(radians(lat2)) * sin(radians(d_lon/2)) ** 2
    c = 2 * atan2(sqrt(a), sqrt(1-a))
    distance = R * c * 1000  # Convert to meters
    return distance

# Function to calculate heading angle between two points
def calculate_heading(lat1, lon1, lat2, lon2):
    d_lon = lon2 - lon1
    y = sin(radians(d_lon)) * cos(radians(lat2))
    x = cos(radians(lat1)) * sin(radians(lat2)) - sin(radians(lat1)) * cos(radians(lat2)) * cos(radians(d_lon))
    heading = degrees(atan2(y, x))
    return heading

# Function to preprocess GPS data
def preprocess_gps_data(gps_data):
    df = pd.DataFrame(gps_data)
    
    # Ensure numeric conversion
    df['Time_Step'] = pd.to_numeric(df['Time_Step'], errors='coerce')
    df['Latitude'] = pd.to_numeric(df['Latitude'], errors='coerce')
    df['Longitude'] = pd.to_numeric(df['Longitude'], errors='coerce')
    
    # Drop rows with failed conversion
    df = df.dropna(subset=['Time_Step', 'Latitude', 'Longitude'])
    
    # Calculate differences for time, latitude, and longitude
    df['Time_Diff'] = df['Time_Step'].diff().fillna(0)
    df['Lat_Diff'] = df['Latitude'].diff().fillna(0)
    df['Lon_Diff'] = df['Longitude'].diff().fillna(0)

    # Calculate Speed (m/s) using Haversine distance and time difference
    df['Speed(m/s)'] = df.apply(lambda row: haversine(
        row['Latitude'], row['Longitude'],
        row['Latitude'] - row['Lat_Diff'], row['Longitude'] - row['Lon_Diff']
    ) / row['Time_Diff'] if row['Time_Diff'] != 0 else 0, axis=1)

    # Calculate Heading Change (degrees)
    df['Heading'] = df.apply(lambda row: calculate_heading(
        row['Latitude'] - row['Lat_Diff'], row['Longitude'] - row['Lon_Diff'],
        row['Latitude'], row['Longitude']
    ) if row.name != 0 else 0, axis=1)
    df['Heading_Change(degrees)'] = df['Heading'].diff().fillna(0)

    # Calculate Acceleration (m/s^2)
    df['Acceleration(m/s^2)'] = (
        df['Speed(m/s)'].diff() / df['Time_Diff'].replace(0, pd.NA).fillna(1).infer_objects(copy=False)
    )

    # Calculate Jerk (m/s^3)
    df['Jerk(m/s^3)'] = (
        df['Acceleration(m/s^2)'].diff() / df['Time_Diff'].replace(0, pd.NA).fillna(1).infer_objects(copy=False)
    )

    # Fill NaN values with 0 (after diff operations)
    df = df.fillna(0)

    
    def calculate_driving_score(row):
        # Adjusted thresholds for Indian driving conditions
        speed_score = min(max(row['Speed(m/s)'] / 11.11, 0), 1)  # Normalize to 0-1, with 11.11 m/s (~40 km/h) as safe speed
        accel_score = min(max(abs(row['Acceleration(m/s^2)']) / 2, 0), 1)  # Normalize to 0-1, with 2 m/s^2 being high acceleration
        heading_score = min(max(abs(row['Heading_Change(degrees)']) / 60, 0), 1)  # Normalize to 0-1, with 60 degrees as significant change
        jerk_score = min(max(abs(row['Jerk(m/s^3)']) / 1.5, 0), 1)  # Normalize to 0-1, with 1.5 m/s^3 being significant jerk

     
        score = (0.4 * speed_score + 0.3 * accel_score + 0.2 * heading_score + 0.1 * jerk_score) * 100
        return score

    df['Driving_Score'] = df.apply(calculate_driving_score, axis=1)

    
    def categorize_driving_score(score):
        if score < 30:
            return 'Safe'
        elif 30 <= score < 70:
            return 'Moderate'
        else:
            return 'Aggressive'

    df['Driving_Category'] = df['Driving_Score'].apply(categorize_driving_score)

    return df[['Speed(m/s)', 'Acceleration(m/s^2)', 'Heading_Change(degrees)', 'Jerk(m/s^3)', 'Driving_Score', 'Driving_Category']]
