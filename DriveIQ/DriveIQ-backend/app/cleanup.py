from app.db import db, AggregatedData
import logging

def cleanup_invalid_aggregated_data(driver_id, date_to_clean):
    try:
        # Find all entries with null driving_score or driving_category for the given driver and date
        invalid_entries = AggregatedData.query.filter_by(driver_id=driver_id, date=date_to_clean).filter(
            (AggregatedData.driving_score == None) | (AggregatedData.driving_category == None)
        ).all()

        # Log the entries that are going to be removed
        if not invalid_entries:
            logging.info(f"No invalid entries found for driver {driver_id} on {date_to_clean}.")
            return

        logging.info(f"Found {len(invalid_entries)} invalid entries to delete for driver {driver_id} on {date_to_clean}.")

        # Delete invalid entries
        for entry in invalid_entries:
            db.session.delete(entry)

        db.session.commit()
        logging.info(f"Invalid entries for driver {driver_id} on {date_to_clean} have been deleted.")
    
    except Exception as e:
        db.session.rollback()
        logging.error(f"Error occurred while cleaning up invalid data: {str(e)}")

# Call this function with the driver ID and the specific date to clean up
cleanup_invalid_aggregated_data(driver_id=1, date_to_clean='2024-10-02')
