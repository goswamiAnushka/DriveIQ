import sys
import os
from flask import Flask, jsonify

# Get the absolute path to the directory containing `DriveIQ-backend`
base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

# Add `DriveIQ-backend` to the system path so that `api` and `utils` can be imported
sys.path.append(base_dir)

# Import the blueprint for the API routes
from api.routes import api_bp

# Initialize the Flask application
app = Flask(__name__)

# Register the API blueprint with an optional URL prefix
app.register_blueprint(api_bp, url_prefix='/api')

# Health check route to verify if the server is running
@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({"status": "Running"}), 200

if __name__ == '__main__':
    # Run the Flask development server with debug enabled
    app.run(debug=True, host='0.0.0.0', port=5000)
