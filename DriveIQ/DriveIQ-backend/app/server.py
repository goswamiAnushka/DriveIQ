import sys
import os

# Add the DriveIQ-backend directory to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from api.routes import api_bp
from flask import Flask

app = Flask(__name__)
app.register_blueprint(api_bp)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
