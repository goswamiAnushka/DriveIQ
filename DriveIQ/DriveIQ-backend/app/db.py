from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Driver(db.Model):
    __tablename__ = 'driver'  # Explicitly define the table name
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Trip(db.Model):
    __tablename__ = 'trip'  # Explicitly define the table name
    id = db.Column(db.Integer, primary_key=True)
    driver_id = db.Column(db.Integer, db.ForeignKey('driver.id'), nullable=False)
    trip_id = db.Column(db.String(50), nullable=False)
    gps_data = db.Column(db.Text, nullable=False)
    score = db.Column(db.Float, nullable=False)
    category = db.Column(db.String(50), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    driver = db.relationship('Driver', backref=db.backref('trips', lazy=True))

class AggregatedData(db.Model):
    __tablename__ = 'aggregated_data'  # Explicitly define the table name
    id = db.Column(db.Integer, primary_key=True)
    driver_id = db.Column(db.Integer, db.ForeignKey('driver.id'), nullable=False)  # Corrected to reference 'driver'
    total_trips = db.Column(db.Integer)
    average_score = db.Column(db.Float)
    risk_level = db.Column(db.String(50))
    aggregated_factors = db.Column(db.Text)
    created_at = db.Column(db.DateTime, nullable=False)
