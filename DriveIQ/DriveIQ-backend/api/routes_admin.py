from flask import Blueprint, jsonify, send_file
from app.db import db, Driver, Trip
from utils.bulk_data_processing import process_bulk_data
from utils.report_generator import generate_pdf_report, generate_excel_report
from io import BytesIO

admin_bp = Blueprint('admin', __name__)

# Admin route to get all drivers
@admin_bp.route('/drivers', methods=['GET'])
def get_all_drivers():
    drivers = Driver.query.all()
    driver_list = [{"id": driver.id, "name": driver.name} for driver in drivers]
    return jsonify(driver_list), 200

# Admin route to get a specific driver's data
@admin_bp.route('/driver/<int:driver_id>', methods=['GET'])
def get_driver_data(driver_id):
    driver = Driver.query.get(driver_id)
    if not driver:
        return jsonify({"error": "Driver not found"}), 404

    processed_data = process_bulk_data(driver_id)
    total_trips = Trip.query.filter_by(driver_id=driver_id).count()
    average_score = processed_data.get('average_score', "No data")

    return jsonify({
        "driver_id": driver.id,
        "name": driver.name,
        "total_trips": total_trips,
        "average_score": average_score,
        "aggregated_factors": processed_data
    }), 200

# Generate PDF report for a driver
@admin_bp.route('/report/pdf/<int:driver_id>', methods=['GET'])
def generate_pdf(driver_id):
    driver = Driver.query.get(driver_id)
    if not driver:
        return jsonify({"error": "Driver not found"}), 404

    report_data = {
        "name": driver.name,
        "total_trips": Trip.query.filter_by(driver_id=driver_id).count(),
        "average_score": process_bulk_data(driver_id).get('average_score', "No data"),
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
        "average_score": process_bulk_data(driver_id).get('average_score', "No data"),
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
            "average_score": process_bulk_data(driver.id).get('average_score', 0)
        }
        for driver in drivers
    ]

    # Sort by average score
    driver_scores = sorted(driver_scores, key=lambda x: x['average_score'], reverse=True)

    return jsonify(driver_scores), 200
