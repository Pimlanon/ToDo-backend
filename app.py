import os
from flask import Flask, jsonify, Blueprint
from flask_cors import CORS
from pydantic import ValidationError
from errors import AppError
from routes.task_routes import task_bp
from routes.page_routes import page_bp
from routes.connection_routes import connection_bp
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

CORS(app, resources={
    r"/*": {
        "origins": [
            os.getenv("FRONTEND_URL"),
            os.getenv("FRONTEND_URL_LOCAL"),
        ]
    }
})

api_bp = Blueprint("api", __name__, url_prefix="/api")

api_bp.register_blueprint(task_bp, url_prefix="/tasks")
api_bp.register_blueprint(page_bp, url_prefix="/pages")
api_bp.register_blueprint(connection_bp, url_prefix="/connections")
app.register_blueprint(api_bp)

# handle error (pydantic)
@app.errorhandler(ValidationError)
def handle_validation_error(e):
    first = e.errors()[0]
    field = first["loc"][0] # filed name : status, title
    msg = first["msg"] # message : Field required
    return jsonify({
        "code": 400,
        "error": f"{msg} {field}" # output: Field required status
    }), 400

# custom error
@app.errorhandler(AppError)
def handle_app_error(e):
    return jsonify(e.to_dict()), e.status_code

# default error
@app.errorhandler(Exception)
def handle_unknown_error(e):
    print(e)
    return jsonify({
        "error": "Internal Server Error",
        "code": 500
    }), 500

# for checking Render (deploy web) connection
@app.route("/")
def home():
    return "Turso + Flask is working!"
