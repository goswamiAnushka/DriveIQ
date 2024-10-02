from flask import Blueprint, jsonify, send_file, request
from app.db import db, Driver, Trip,AggregatedData
from utils.bulk_data_processing import process_bulk_data
from utils.ml_integration import predict_bulk_driver_behavior
import logging
from io import BytesIO

admin_bp = Blueprint('admin', __name__)

# Admin route to get all drivers
@admin_bp.route('/drivers', methods=['GET'])
def get_all_drivers():
    drivers = Driver.query.all()
    driver_list = [{"id": driver.id, "name": driver.name} for driver in drivers]
    logging.info(f"Admin retrieved all drivers: {driver_list}")
    return jsonify(driver_list), 200

# Admin route to get all daily data for a driver until the current date
@admin_bp.route('/driver/all_daily_data/<int:driver_id>', methods=['GET'])
def get_all_daily_driver_data(driver_id):
    try:
        # Query all daily aggregated data for the given driver
        daily_data = AggregatedData.query.filter_by(driver_id=driver_id).order_by(AggregatedData.date).all()

        if not daily_data:
            return jsonify({"error": f"No data found for driver {driver_id}."}), 404

        # Group and format the daily data
        grouped_data = {}
        for data in daily_data:
            day = str(data.date)
            if day not in grouped_data:
                grouped_data[day] = []
            grouped_data[day].append({
                'avg_speed': data.avg_speed,
                'avg_acceleration': data.avg_acceleration,
                'avg_jerk': data.avg_jerk,
                'avg_heading_change': data.avg_heading_change,
                'avg_braking_intensity': data.avg_braking_intensity,
                'avg_sasv': data.avg_sasv,
                'speed_violation_count': data.speed_violation_count,
                'total_observations': data.total_observations,
                'driving_score': data.driving_score,  # Fetch driving score
                'driving_category': data.driving_category  # Fetch driving category
            })

        # Format and return the data grouped by date
        return jsonify({
            "driver_id": driver_id,
            "daily_data": grouped_data
        }), 200

    except Exception as e:
        logging.error(f"Error fetching daily data for driver {driver_id}: {str(e)}")
        return jsonify({"error": "An error occurred while fetching daily data"}), 500


@admin_bp.route('/driver/bulk_consolidated_data/<int:driver_id>', methods=['GET'])
def get_bulk_consolidated_driver_data(driver_id):
    try:
        # Query all daily aggregated data for the given driver
        daily_aggregates = AggregatedData.query.filter_by(driver_id=driver_id).order_by(AggregatedData.date).all()

        if not daily_aggregates:
            return jsonify({"error": f"No daily data found for driver {driver_id}."}), 404

        # Initialize dictionary to accumulate aggregated factors
        total_data = {
            'Speed(m/s)_mean': 0,
            'Acceleration(m/s^2)_mean': 0,
            'Jerk(m/s^3)_mean': 0,
            'Heading_Change(degrees)_mean': 0,
            'Braking_Intensity_mean': 0,
            'SASV_total': 0,
            'Speed_Violation_total': 0,
            'Total_Observations': 0
        }
        total_score = 0
        total_days = len(daily_aggregates)

        # Accumulate data from each day's record
        for day_data in daily_aggregates:
            total_data['Speed(m/s)_mean'] += day_data.avg_speed
            total_data['Acceleration(m/s^2)_mean'] += day_data.avg_acceleration
            total_data['Jerk(m/s^3)_mean'] += day_data.avg_jerk
            total_data['Heading_Change(degrees)_mean'] += day_data.avg_heading_change
            total_data['Braking_Intensity_mean'] += day_data.avg_braking_intensity
            total_data['SASV_total'] += day_data.avg_sasv
            total_data['Speed_Violation_total'] += day_data.speed_violation_count
            total_data['Total_Observations'] += day_data.total_observations
            total_score += day_data.driving_score  # Accumulate daily driving score

        # Calculate averages for features
        for key in total_data.keys():
            if key.endswith('_mean'):
                total_data[key] /= total_days

        # Calculate the average score
        avg_driving_score = total_score / total_days

        # Send consolidated data to the bulk ML model (if needed)
        driving_category, driving_score = predict_bulk_driver_behavior([total_data])

        # You can choose to either use the score predicted by the ML model or the averaged score from daily data.
        # For now, we return the averaged daily score as well.
        return jsonify({
            "aggregated_data": total_data,
            "driving_category": driving_category,
            "average_driving_score": avg_driving_score,  # Average of daily driving scores
            "model_predicted_score": driving_score  # Predicted score from the model
        }), 200

    except Exception as e:
        logging.error(f"Error during bulk prediction for driver {driver_id}: {str(e)}")
        return jsonify({"error": "An error occurred while processing bulk data"}), 500
