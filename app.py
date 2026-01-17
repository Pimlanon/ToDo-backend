from flask import Flask, jsonify, Blueprint
from flask_cors import CORS
from werkzeug.exceptions import HTTPException
from pydantic import ValidationError
from errors import AppError
from routes.user_routes import user_bp
from routes.task_routes import task_bp
from routes.page_routes import page_bp

app = Flask(__name__)

CORS(app)

api_bp = Blueprint("api", __name__, url_prefix="/api")

api_bp.register_blueprint(user_bp, url_prefix="/users")
api_bp.register_blueprint(task_bp, url_prefix="/tasks")
api_bp.register_blueprint(page_bp, url_prefix="/pages")
app.register_blueprint(api_bp)

# handle error (pydantic)
@app.errorhandler(ValidationError)
def handle_validation_error(e):
    first = e.errors()[0]
    return jsonify({
        "code": 400,
        "field": first["loc"][0],
        "error": first["msg"]
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
