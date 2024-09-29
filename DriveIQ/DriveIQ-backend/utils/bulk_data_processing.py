import os
import pandas as pd
import numpy as np
import json
import logging
from app.db import Trip
from math import radians, sin, cos, atan2, degrees ,sqrt
import osmnx as ox

# Set up logging
logging.basicConfig(level=logging.INFO)

# Haversine formula to calculate distance between two GPS points
def haversine(lat1, lon1, lat2, lon2):
    R = 6371000  # Earth's radius in meters
    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])
    d_lat = lat2 - lat1
    d_lon = lon1 - lon2
    a = sin(d_lat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(d_lon / 2) ** 2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    return R * c  # Distance in meters

# Calculate heading change between two GPS points
def calculate_heading(lat1, lon1, lat2, lon2):
    d_lon = lon1 - lon2
    x = cos(radians(lat2)) * sin(radians(d_lon))
    y = cos(radians(lat1)) * sin(radians(lat2)) - sin(radians(lat1)) * cos(radians(lat2)) * cos(radians(d_lon))
    initial_heading = atan2(x, y)
    return (degrees(initial_heading) + 360) % 360  # Normalize heading to [0, 360]

def fetch_sensitive_areas(lat, lon, radius=300):
    try:
        if not (-90 <= lat <= 90) or not (-180 <= lon <= 180):
            raise ValueError(f"Invalid coordinates: Latitude = {lat}, Longitude = {lon}")

        tags = {'amenity': ['school', 'hospital']}
        logging.info(f"Fetching sensitive areas for coordinates: ({lat}, {lon}) with tags: {tags} and radius: {radius}")

        sensitive_areas = ox.features_from_point((lat, lon), tags, dist=radius)

        if sensitive_areas.empty:
            logging.warning("No sensitive areas found. Applying default logic.")
            return []

        sensitive_coords = sensitive_areas['geometry'].apply(lambda x: (x.centroid.y, x.centroid.x))
        return sensitive_coords.tolist()
    except Exception as e:
        logging.error(f"Error fetching sensitive areas: {str(e)}")
        return []

def calculate_sasv(lat, lon, speed, sensitive_locations):
    if not sensitive_locations:
        logging.info("No sensitive areas found, skipping SASV calculation.")
        return 0  # No risk if no sensitive areas are found

    distances = [haversine(lat, lon, s_lat, s_lon) for s_lat, s_lon in sensitive_locations]
    if any(dist < 300 for dist in distances) and speed > 8.33:  # ~30 km/h speed limit in sensitive areas
        return 1
    return 0

def process_gps_data(gps_data):
    if not gps_data or len(gps_data) < 2:
        raise ValueError("Insufficient GPS data")

    df = pd.DataFrame(gps_data)
    required_columns = ['Latitude', 'Longitude', 'Time_Step']

    # Check for required columns
    for col in required_columns:
        if col not in df.columns:
            raise ValueError(f"Missing required column: {col}")

    df['Latitude'] = pd.to_numeric(df['Latitude'], errors='coerce')
    df['Longitude'] = pd.to_numeric(df['Longitude'], errors='coerce')
    df['Time_Step'] = pd.to_numeric(df['Time_Step'], errors='coerce')

    # Drop any rows with missing values
    df.dropna(subset=['Latitude', 'Longitude', 'Time_Step'], inplace=True)

    if len(df) < 2:
        raise ValueError("Insufficient valid GPS data after cleaning")

    # Calculate distance and speed
    df['Lat_Shifted'] = df['Latitude'].shift(1)
    df['Lon_Shifted'] = df['Longitude'].shift(1)
    df['Distance(m)'] = df.apply(lambda row: haversine(row['Lat_Shifted'], row['Lon_Shifted'], row['Latitude'], row['Longitude']), axis=1)

    df['Time_Diff(s)'] = df['Time_Step'].diff().fillna(1)
    df['Time_Diff(s)'] = df['Time_Diff(s)'].apply(lambda x: max(x, 1))

    df['Speed(m/s)'] = df['Distance(m)'] / df['Time_Diff(s)']
    df['Speed(km/h)'] = df['Speed(m/s)'] * 3.6

    # Filter out rows where the speed is below 5 km/h
    df = df[df['Speed(km/h)'] > 5]

    if df.empty:
        raise ValueError("No valid movement data after filtering low speeds")

    # Calculate acceleration, jerk, heading change, and braking intensity
    df['Acceleration(m/s^2)'] = df['Speed(m/s)'].diff() / df['Time_Diff(s)']
    df['Jerk(m/s^3)'] = df['Acceleration(m/s^2)'].diff() / df['Time_Diff(s)']
    df['Heading'] = df.apply(lambda row: calculate_heading(row['Lat_Shifted'], row['Lon_Shifted'], row['Latitude'], row['Longitude']), axis=1)
    df['Heading_Change(degrees)'] = df['Heading'].diff().fillna(0)
    df['Braking_Intensity'] = df['Acceleration(m/s^2)'].apply(lambda x: abs(x) if x < 0 else 0)

    # Sensitive area speed violation
    df['SASV'] = df.apply(lambda row: calculate_sasv(row['Latitude'], row['Longitude'], row['Speed(m/s)'], fetch_sensitive_areas(row['Latitude'], row['Longitude'])), axis=1)

    # Speed violation
    df['Speed_Violation'] = df['Speed(km/h)'].apply(lambda x: 1 if x > 50 else 0)

    # Aggregate metrics
    return {
        'avg_speed': df['Speed(m/s)'].mean(),
        'avg_acceleration': df['Acceleration(m/s^2)'].mean(),
        'avg_jerk': df['Jerk(m/s^3)'].mean(),
        'avg_heading_change': df['Heading_Change(degrees)'].mean(),
        'avg_braking_intensity': df['Braking_Intensity'].mean(),
        'SASV': df['SASV'].sum(),  # Sum of SASV
        'Speed_Violation': df['Speed_Violation'].sum()  # Sum of Speed Violations
    }

def process_bulk_data(driver_id, end_date=None):
    trips = Trip.query.filter(Trip.driver_id == driver_id).all()

    if not trips:
        return {"error": "No trips found for this driver."}

    aggregated_data = {
        'Speed(m/s)_mean': 0,
        'Speed(m/s)_max': 0,
        'Speed(m/s)_std': 0,
        'Acceleration(m/s^2)_mean': 0,
        'Acceleration(m/s^2)_max': 0,
        'Acceleration(m/s^2)_std': 0,
        'Heading_Change(degrees)_mean': 0,
        'Heading_Change(degrees)_max': 0,
        'Heading_Change(degrees)_std': 0,
        'Jerk(m/s^3)_mean': 0,
        'Jerk(m/s^3)_max': 0,
        'Jerk(m/s^3)_std': 0,
        'Braking_Intensity_mean': 0,
        'Braking_Intensity_max': 0,
        'Braking_Intensity_std': 0,
        'SASV_total': 0,
        'Speed_Violation_total': 0,
        'Total_Observations': 0,
    }

    for trip in trips:
        gps_data = json.loads(trip.gps_data)
        try:
            processed_data = process_gps_data(gps_data)

            logging.info(f"Processed Data for Trip {trip.trip_id}: {processed_data}")

            # Aggregate metrics
            aggregated_data['Speed(m/s)_mean'] += processed_data['avg_speed']
            aggregated_data['Acceleration(m/s^2)_mean'] += processed_data['avg_acceleration']
            aggregated_data['Jerk(m/s^3)_mean'] += processed_data['avg_jerk']
            aggregated_data['Heading_Change(degrees)_mean'] += processed_data['avg_heading_change']
            aggregated_data['Braking_Intensity_mean'] += processed_data['avg_braking_intensity']
            aggregated_data['SASV_total'] += processed_data['SASV']
            aggregated_data['Speed_Violation_total'] += processed_data['Speed_Violation']
            aggregated_data['Total_Observations'] += 1
            
        except ValueError as e:
            logging.warning(f"Skipping trip {trip.trip_id} due to error: {str(e)}")

    if aggregated_data['Total_Observations'] == 0:
        return {"error": "No valid data found for this driver."}

    # Finalize calculations for averages and standard deviations
    for key in aggregated_data.keys():
        if key.endswith('_mean'):
            aggregated_data[key] /= aggregated_data['Total_Observations']

    logging.info(f"Aggregated Data for Driver {driver_id}: {aggregated_data}")

    return aggregated_data  # Return the full aggregated data