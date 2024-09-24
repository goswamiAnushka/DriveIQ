import pandas as pd
from app.db import Trip

def process_bulk_data(driver_id):
    """
    Processes bulk data for a driver by aggregating data from all their trips and calculating various driving metrics.
    """
    # Fetch all trips for the driver
    trips = Trip.query.filter_by(driver_id=driver_id).all()

    trip_data = []
    for trip in trips:
        # Convert stored GPS data string back to DataFrame
        processed_data = pd.DataFrame(eval(trip.gps_data))

        # Skip trips without 'Driving_Score' or other necessary features
        if 'Driving_Score' not in processed_data.columns:
            continue

        trip_data.append(processed_data)

    # If no valid trip data is found
    if not trip_data:
        return {"error": "No valid trips with 'Driving_Score' found for this driver"}

    # Concatenate all valid trip data into a single DataFrame
    bulk_data = pd.concat(trip_data)

    # Extract and calculate all the necessary driving metrics (features)
    features = {
        'Speed(m/s)_mean': bulk_data['Speed(m/s)'].mean(),
        'Speed(m/s)_max': bulk_data['Speed(m/s)'].max(),
        'Speed(m/s)_std': bulk_data['Speed(m/s)'].std(),

        'Acceleration(m/s^2)_mean': bulk_data['Acceleration(m/s^2)'].mean(),
        'Acceleration(m/s^2)_max': bulk_data['Acceleration(m/s^2)'].max(),
        'Acceleration(m/s^2)_std': bulk_data['Acceleration(m/s^2)'].std(),

        'Heading_Change(degrees)_mean': bulk_data['Heading_Change(degrees)'].mean(),
        'Heading_Change(degrees)_std': bulk_data['Heading_Change(degrees)'].std(),

        'Jerk(m/s^3)_mean': bulk_data['Jerk(m/s^3)'].mean(),
        'Jerk(m/s^3)_max': bulk_data['Jerk(m/s^3)'].max(),
        'Jerk(m/s^3)_std': bulk_data['Jerk(m/s^3)'].std(),

        'Braking_Intensity_mean': bulk_data['Braking_Intensity'].mean(),
        'Braking_Intensity_max': bulk_data['Braking_Intensity'].max(),

        'SASV_mean': bulk_data['SASV'].mean(),
        'SASV_total': bulk_data['SASV'].sum(),

        'Speed_Violation_mean': bulk_data['Speed_Violation'].mean(),
        'Speed_Violation_total': bulk_data['Speed_Violation'].sum(),

        'Driving_Score_mean': bulk_data['Driving_Score'].mean(),
        'Total_Observations': len(bulk_data)
    }

    return features
