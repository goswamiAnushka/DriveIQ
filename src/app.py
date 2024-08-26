# src/app.py
from flask import Flask
from api.routes import api_routes

app = Flask(__name__)
app.register_blueprint(api_routes)

if __name__ == "__main__":
    app.run(debug=True)
