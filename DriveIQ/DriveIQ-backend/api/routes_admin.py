from flask import Blueprint, jsonify, send_file, request
from app.db import db, Driver, Trip
from utils.bulk_data_processing import process_bulk_data
from utils.report_generator import generate_pdf_report, generate_excel_report
from utils.ml_integration import predict_bulk_driver_behavior
import logging
from io import BytesIO


admin_bp = Blueprint('admin', __name__)

# Admin route to get all drivers
@admin_bp.route('/drivers', methods=['GET'])
def get_all_drivers():
    drivers = Driver.query.all()
    driver_list = [{"id": driver.id, "name": driver.name} for driver in drivers]
    return jsonify(driver_list), 200

# Admin route to get bulk data for a driver
@admin_bp.route('/driver/bulk_data/<int:driver_id>', methods=['GET'])
def get_bulk_driver_data(driver_id):
    try:
        # Process bulk data based on aggregated daily data
        processed_data = process_bulk_data(driver_id)

        # Check if any errors occurred during processing
        if 'error' in processed_data:
            return jsonify({"error": processed_data['error']}), 400

        # Extract features for prediction
        bulk_features = {
            'Speed(m/s)_mean': processed_data['Speed(m/s)_mean'],
            'Acceleration(m/s^2)_mean': processed_data['Acceleration(m/s^2)_mean'],
            'Jerk(m/s^3)_mean': processed_data['Jerk(m/s^3)_mean'],
            'Heading_Change(degrees)_mean': processed_data['Heading_Change(degrees)_mean'],
            'Braking_Intensity_mean': processed_data['Braking_Intensity_mean'],
            'SASV_total': processed_data['SASV_total'],
            'Total_Observations': processed_data['Total_Observations']
        }

        # Pass the aggregated data to the ML model for scoring
        driving_category, driving_score = predict_bulk_driver_behavior(bulk_features)

        return jsonify({
            "category": driving_category,
            "driving_score": driving_score,
            "aggregated_data": bulk_features
        }), 200

    except Exception as e:
        logging.error(f"Error during bulk prediction: {str(e)}")
        return jsonify({"error": "An error occurred while processing bulk data"}), 500
# Generate PDF report for a driver
@admin_bp.route('/report/pdf/<int:driver_id>', methods=['GET'])
def generate_pdf(driver_id):
    driver = Driver.query.get(driver_id)
    if not driver:
        return jsonify({"error": "Driver not found"}), 404

    report_data = {
        "name": driver.name,
        "total_trips": Trip.query.filter_by(driver_id=driver_id).count(),
        "average_score": process_bulk_data(driver_id).get('avg_speed', "No data"),
        "trips": [{"trip_id": trip.trip_id, "score": trip.score} for trip in driver.trips]
    }

    pdf_file = BytesIO()
    generate_pdf_report(report_data, pdf_file)
    pdf_file.seek(0)

    return send_file(pdf_file, mimetype='application/pdf', as_attachment=True, download_name=f"driver_{driver.name}_report.pdf")

# Generate Excel report for a driver
@admin_bp.route('/report/excel/<int:driver_id>', methods=['GET'])
def generate_excel(driver_id):
    driver = Driver.query.get(driver_id)
    if not driver:
        return jsonify({"error": "Driver not found"}), 404

    report_data = {
        "name": driver.name,
        "total_trips": Trip.query.filter_by(driver_id=driver_id).count(),
        "average_score": process_bulk_data(driver_id).get('avg_speed', "No data"),
        "trips": [{"trip_id": trip.trip_id, "score": trip.score} for trip in driver.trips]
    }

    excel_file = BytesIO()
    generate_excel_report(report_data, excel_file)
    excel_file.seek(0)

    return send_file(excel_file, mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet', as_attachment=True, download_name=f"driver_{driver.name}_report.xlsx")

# Leaderboard: Get drivers ranked by their scores
@admin_bp.route('/leaderboard', methods=['GET'])
def leaderboard():
    drivers = Driver.query.all()
    driver_scores = [
        {
            "id": driver.id,
            "name": driver.name,
            "average_score": process_bulk_data(driver.id).get('avg_speed', 0)
        }
        for driver in drivers
    ]

    # Sort by average score
    driver_scores = sorted(driver_scores, key=lambda x: x['average_score'], reverse=True)

    return jsonify(driver_scores), 200
