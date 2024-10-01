import logging
from app.db import AggregatedData
from sqlalchemy import func

# Bulk data processing logic using daily aggregated data
def process_bulk_data(driver_id):
    try:
        # Query all daily aggregated data for the given driver
        daily_aggregates = AggregatedData.query.filter_by(driver_id=driver_id).all()

        if not daily_aggregates:
            return {"error": "No daily data found for this driver."}

        # Initialize aggregation dictionary
        aggregated_data = {
            'Speed(m/s)_mean': 0,
            'Acceleration(m/s^2)_mean': 0,
            'Jerk(m/s^3)_mean': 0,
            'Heading_Change(degrees)_mean': 0,
            'Braking_Intensity_mean': 0,
            'SASV_total': 0,
            'Speed_Violation_total': 0,
            'Total_Observations': 0
        }

        total_days = len(daily_aggregates)
        for daily in daily_aggregates:
            aggregated_data['Speed(m/s)_mean'] += daily.avg_speed
            aggregated_data['Acceleration(m/s^2)_mean'] += daily.avg_acceleration
            aggregated_data['Jerk(m/s^3)_mean'] += daily.avg_jerk
            aggregated_data['Heading_Change(degrees)_mean'] += daily.avg_heading_change
            aggregated_data['Braking_Intensity_mean'] += daily.avg_braking_intensity
            aggregated_data['SASV_total'] += daily.avg_sasv
            aggregated_data['Speed_Violation_total'] += daily.speed_violation_count
            aggregated_data['Total_Observations'] += daily.total_observations

        # Take averages over the total days
        for key in aggregated_data.keys():
            if key.endswith('_mean'):
                aggregated_data[key] /= total_days

        logging.info(f"Aggregated Data for Driver {driver_id}: {aggregated_data}")

        return aggregated_data

    except Exception as e:
        logging.error(f"Error in bulk data processing for driver {driver_id}: {str(e)}")
        return {"error": "An error occurred during bulk processing."}
