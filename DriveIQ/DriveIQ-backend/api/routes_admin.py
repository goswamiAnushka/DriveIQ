from flask import Blueprint, jsonify
from app.db import db, Driver, Trip, AggregatedData
from utils.bulk_data_processing import process_bulk_data

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
