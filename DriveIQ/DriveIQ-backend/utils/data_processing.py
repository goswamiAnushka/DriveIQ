import pandas as pd
import numpy as np
from math import radians, sin, cos, sqrt, atan2, degrees
import osmnx as ox

# Haversine formula to calculate distance between two GPS points
def haversine(lat1, lon1, lat2, lon2):
    R = 6371000  # Earth's radius in meters
    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])
    d_lat = lat2 - lat1
    d_lon = lon2 - lon1
    a = sin(d_lat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(d_lon / 2) ** 2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    return R * c  # Distance in meters

# Calculate heading change between two GPS points
def calculate_heading(lat1, lon1, lat2, lon2):
    d_lon = lon2 - lon1
    x = cos(radians(lat2)) * sin(radians(d_lon))
    y = cos(radians(lat1)) * sin(radians(lat2)) - sin(radians(lat1)) * cos(radians(lat2)) * cos(radians(d_lon))
    initial_heading = atan2(x, y)
    return (degrees(initial_heading) + 360) % 360  # Normalize heading to [0, 360]

# Fetch sensitive areas (schools, hospitals) from OpenStreetMap
def fetch_sensitive_areas(lat, lon, radius=300):
    try:
        if not (-90 <= lat <= 90) or not (-180 <= lon <= 180):
            raise ValueError(f"Invalid coordinates: Latitude = {lat}, Longitude = {lon}")

        tags = {'amenity': ['school', 'hospital']}
        sensitive_areas = ox.features_from_point((lat, lon), tags, dist=radius)

        if sensitive_areas.empty:
            print(f"No sensitive areas found for location: ({lat}, {lon}) with radius {radius} meters.")
            return []

        sensitive_coords = sensitive_areas['geometry'].apply(lambda x: (x.centroid.y, x.centroid.x))
        return sensitive_coords.tolist()
    except Exception as e:
        print(f"Error fetching sensitive areas: {str(e)}")
        return []

# Calculate sensitive area speed violation (SASV)
def calculate_sasv(lat, lon, speed, sensitive_locations):
    distances = [haversine(lat, lon, s_lat, s_lon) for s_lat, s_lon in sensitive_locations]
    if any(dist < 300 for dist in distances) and speed > 8.33:  # ~30 km/h speed limit in sensitive areas
        return 1
    return 0

# Process GPS data and calculate metrics
def process_gps_data(gps_data):
    df = pd.DataFrame(gps_data)

    if df.empty:
        raise ValueError("GPS data is empty")

    required_columns = ['Latitude', 'Longitude', 'Time_Step']
    for col in required_columns:
        if col not in df.columns:
            raise ValueError(f"Missing required column: {col}")

    # Convert necessary columns to numeric
    df['Latitude'] = pd.to_numeric(df['Latitude'], errors='coerce')
    df['Longitude'] = pd.to_numeric(df['Longitude'], errors='coerce')
    df['Time_Step'] = pd.to_numeric(df['Time_Step'], errors='coerce')

    # Drop rows with missing or invalid values
    df.dropna(subset=['Latitude', 'Longitude', 'Time_Step'], inplace=True)

    # Shift latitude and longitude for calculating distance and heading
    df['Lat_Shifted'] = df['Latitude'].shift(1)
    df['Lon_Shifted'] = df['Longitude'].shift(1)

    # Calculate distance between consecutive points
    df['Distance(m)'] = df.apply(lambda row: haversine(row['Lat_Shifted'], row['Lon_Shifted'], row['Latitude'], row['Longitude']), axis=1)

    # Calculate time difference between consecutive points
    df['Time_Diff(s)'] = df['Time_Step'].diff().fillna(1)

    # Calculate speed as distance/time
    df['Speed(m/s)'] = df['Distance(m)'] / df['Time_Diff(s)']

    # Filter out invalid speed calculations
    df.replace([np.inf, -np.inf], np.nan, inplace=True)
    df.dropna(subset=['Speed(m/s)'], inplace=True)

    # Calculate acceleration
    df['Acceleration(m/s^2)'] = df['Speed(m/s)'].diff() / df['Time_Diff(s)']

    # Calculate braking intensity
    df['Braking_Intensity'] = df['Acceleration(m/s^2)'].apply(lambda x: abs(x) if x < 0 else 0)

    # Calculate heading change between consecutive points
    df['Heading'] = df.apply(lambda row: calculate_heading(row['Lat_Shifted'], row['Lon_Shifted'], row['Latitude'], row['Longitude']), axis=1)
    df['Heading_Change(degrees)'] = df['Heading'].diff().fillna(0)

    # Calculate jerk (rate of change of acceleration)
    df['Jerk(m/s^3)'] = df['Acceleration(m/s^2)'].diff() / df['Time_Diff(s)']

    # Calculate sensitive area speed violations (SASV)
    df['SASV'] = df.apply(lambda row: calculate_sasv(row['Latitude'], row['Longitude'], row['Speed(m/s)'], fetch_sensitive_areas(row['Latitude'], row['Longitude'])), axis=1)

    # Calculate speed violations (general speed limits)
    def calculate_speed_violation(row):
        return 1 if row['Speed(m/s)'] > 13.89 else 0  # 13.89 m/s (~50 km/h) general speed limit
    df['Speed_Violation'] = df.apply(calculate_speed_violation, axis=1)

    # Return the processed data
    return df
