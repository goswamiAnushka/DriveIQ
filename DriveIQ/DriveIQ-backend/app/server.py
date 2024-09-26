import sys
import os
from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS  # Enable CORS for cross-origin requests
from flask_socketio import SocketIO, emit  # For enabling real-time WebSocket communication

# Add the root project directory (DriveIQ-backend) to sys.path to resolve other imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.db import db  # Import the db instance from app.db
from api.routes import api_bp  # Import API routes
from api.routes_admin import admin_bp  # Import Admin routes

# Initialize the Flask application
app = Flask(__name__)

# Enable CORS to allow requests from your frontend (React) running on a different domain/port
CORS(app)

# Configure the SQLite database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///driveiq.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize SQLAlchemy and Migrate
db.init_app(app)
migrate = Migrate(app, db)

# Initialize SocketIO for real-time data streaming
socketio = SocketIO(app, cors_allowed_origins="*")

# Register the API blueprint (driver routes)
app.register_blueprint(api_bp, url_prefix='/api')

# Register the Admin blueprint
app.register_blueprint(admin_bp, url_prefix='/admin')

# Health check route to verify if the server is running
@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({"status": "Running"}), 200

# WebSocket event handling
@socketio.on('connect')
def handle_connect():
    print("Client connected!")
    emit('server_response', {'data': 'Connected to WebSocket!'})

@socketio.on('disconnect')
def handle_disconnect():
    print("Client disconnected!")

# GPS WebSocket stream
@socketio.on('gps_update')
def gps_update(data):
    print(f"Received GPS data: {data}")
    emit('gps_response', {'data': 'GPS data received'}, broadcast=True)

if __name__ == "__main__":
    # Run the app using SocketIO to support both HTTP and WebSocket
    socketio.run(app, debug=True, host='0.0.0.0', port=5000)
