import os
import pandas as pd
import numpy as np
from math import radians, sin, cos, sqrt, atan2, degrees
import osmnx as ox  # For OpenStreetMap integration

# Haversine formula to calculate distance between two points
def haversine(lat1, lon1, lat2, lon2):
    R = 6371000  # Earth's radius in meters
    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])

    d_lat = lat2 - lat1
    d_lon = lon2 - lon1

    a = sin(d_lat / 2.0) ** 2 + cos(lat1) * cos(lat2) * sin(d_lon / 2.0) ** 2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    return R * c  # Return distance in meters

# Function to calculate heading change between two GPS points
def calculate_heading(lat1, lon1, lat2, lon2):
    d_lon = lon2 - lon1
    x = cos(radians(lat2)) * sin(radians(d_lon))
    y = cos(radians(lat1)) * sin(radians(lat2)) - sin(radians(lat1)) * cos(radians(lat2)) * cos(radians(d_lon))
    
    initial_heading = atan2(x, y)
    initial_heading = degrees(initial_heading)
    
    # Normalize the heading to [0, 360]
    return (initial_heading + 360) % 360

# Fetch sensitive areas using OSM
def fetch_sensitive_areas(lat, lon, radius=300):
    """
    Fetch sensitive areas (schools, hospitals) using OpenStreetMap within a radius from a given point.
    If no sensitive locations are found, return an empty list.
    """
    try:
        tags = {'amenity': ['school', 'hospital']}
        sensitive_areas = ox.features_from_point((lat, lon), tags, dist=radius)

        if sensitive_areas.empty:
            return []

        # Extract lat/lon of these sensitive areas
        sensitive_coords = sensitive_areas['geometry'].apply(lambda x: (x.centroid.y, x.centroid.x))
        return sensitive_coords.tolist()
    except Exception as e:
        # Log the error (if necessary) and return an empty list if OSM fails to fetch data
        print(f"Error fetching sensitive areas: {str(e)}")
        return []

# Function to calculate SASV (Sensitive Area Speed Violation)
def calculate_sasv(lat, lon, speed, sensitive_locations):
    sensitive_distances = [haversine(lat, lon, s_lat, s_lon) for s_lat, s_lon in sensitive_locations]
    
    if any(dist < 300 for dist in sensitive_distances):  # Within 300 meters of sensitive areas
        if speed > 8.33:  # Speed > 30 km/h in sensitive area
            return 1
    return 0

# Process the GPS data and calculate features like speed, acceleration, heading change, SASV, and violations
def process_gps_data(gps_data):
    df = pd.DataFrame(gps_data)

    if df.empty:
        raise ValueError("GPS data is empty")

    required_columns = ['Latitude', 'Longitude', 'Time_Step']
    for col in required_columns:
        if col not in df.columns:
            raise ValueError(f"Missing required column: {col}")

    # Ensure the numeric data is valid and filled (removes invalid entries)
    df['Latitude'] = pd.to_numeric(df['Latitude'], errors='coerce')
    df['Longitude'] = pd.to_numeric(df['Longitude'], errors='coerce')
    df['Time_Step'] = pd.to_numeric(df['Time_Step'], errors='coerce')
    
    # Drop rows where Latitude, Longitude, or Time_Step are NaN
    df = df.dropna(subset=['Latitude', 'Longitude', 'Time_Step'])

    # Calculate distance between consecutive points using Haversine
    df['Lat_Shifted'] = df['Latitude'].shift(1)
    df['Lon_Shifted'] = df['Longitude'].shift(1)

    # Apply the Haversine function element-wise using .apply
    df['Distance(m)'] = df.apply(lambda row: haversine(row['Lat_Shifted'], row['Lon_Shifted'], row['Latitude'], row['Longitude']), axis=1)

    # Calculate time difference between consecutive points (in seconds)
    df['Time_Diff(s)'] = df['Time_Step'].diff().fillna(1)  # Time difference in seconds

    # Calculate speed (m/s) as distance divided by time difference
    df['Speed(m/s)'] = df['Distance(m)'] / df['Time_Diff(s)']

    # Handle cases where time difference is 0 (which would cause division by zero)
    df.replace([np.inf, -np.inf], np.nan, inplace=True)
    df.dropna(subset=['Speed(m/s)'], inplace=True)

    # Calculate acceleration (m/s^2)
    df['Acceleration(m/s^2)'] = df['Speed(m/s)'].diff() / df['Time_Diff(s)']

    # Calculate braking intensity: absolute value of negative acceleration (deceleration)
    df['Braking_Intensity'] = df['Acceleration(m/s^2)'].apply(lambda x: abs(x) if x < 0 else 0)

    # Calculate heading change
    df['Heading'] = df.apply(lambda row: calculate_heading(row['Lat_Shifted'], row['Lon_Shifted'], row['Latitude'], row['Longitude']), axis=1)
    df['Heading_Change(degrees)'] = df['Heading'].diff().fillna(0)

    # Calculate jerk (m/s^3)
    df['Jerk(m/s^3)'] = df['Acceleration(m/s^2)'].diff() / df['Time_Diff(s)']

    # Calculate SASV for each GPS point
    df['SASV'] = df.apply(lambda row: calculate_sasv(row['Latitude'], row['Longitude'], row['Speed(m/s)'], fetch_sensitive_areas(row['Latitude'], row['Longitude'])), axis=1)

    # Calculate rule violation score for exceeding general speed limit
    def calculate_speed_violation(row):
        speed_limit = 13.89  # ~50 km/h general speed limit
        if row['Speed(m/s)'] > speed_limit:
            return 1  # Speed violation
        return 0
    df['Speed_Violation'] = df.apply(calculate_speed_violation, axis=1)

    # Drop the first row since it has NaN values due to diff()
    df = df.dropna()

    # Return the processed DataFrame
    return df
