from flask import Flask, jsonify
from api.routes import api

def create_app():
    app = Flask(__name__)

    # Register Blueprints
    app.register_blueprint(api, url_prefix='/api')

    @app.route('/')
    def home():
        return jsonify({"message": "Welcome to the DriveIQ API!"}), 200

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True, host='0.0.0.0', port=5000)
