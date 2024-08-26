# src/app.py

from flask import Flask
from api.routes import api_bp

app = Flask(__name__)

# Register the blueprint
app.register_blueprint(api_bp, url_prefix='/api')

if __name__ == "__main__":
    app.run(debug=True)
