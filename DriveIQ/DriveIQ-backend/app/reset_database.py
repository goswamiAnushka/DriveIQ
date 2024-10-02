from app.server import app  # Import the Flask app instance
from app.db import db, Driver, Trip, AggregatedData

def clear_database():
    with app.app_context():  # Use the Flask app instance for context
        db.session.query(Trip).delete()
        db.session.query(Driver).delete()
        db.session.query(AggregatedData).delete()
        db.session.commit()
        print("All records have been cleared.")

if __name__ == '__main__':
    clear_database()
