import sys
import os
from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy  # Make sure SQLAlchemy is imported
from flask_migrate import Migrate

# Add the root project directory (DriveIQ-backend) to sys.path so it can resolve other imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.db import db  # Import the db instance from app.db
from api.routes import api_bp  # Import API routes
from api.routes_admin import admin_bp  # Import Admin routes

# Initialize the Flask application
app = Flask(__name__)

# Configure the SQLite database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///driveiq.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize SQLAlchemy and Migrate
db.init_app(app)  # Initialize the SQLAlchemy instance
migrate = Migrate(app, db)

# Register the API blueprint
app.register_blueprint(api_bp, url_prefix='/api')

# Register the Admin blueprint
app.register_blueprint(admin_bp, url_prefix='/admin')

# Health check route to verify if the server is running
@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({"status": "Running"}), 200

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
