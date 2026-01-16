from flask import Flask, jsonify, Blueprint
from routes.user_routes import user_bp
from werkzeug.exceptions import HTTPException
import traceback
from pydantic import ValidationError

app = Flask(__name__)
api_bp = Blueprint("api", __name__, url_prefix="/api")

api_bp.register_blueprint(user_bp, url_prefix="/users")
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

@app.errorhandler(ValueError)
def handle_value_error(e):
    print(traceback.format_exc())

    return jsonify({
        "error": str(e),
        "code": 409
    }), 409

@app.errorhandler(Exception)
def handle_all_errors(e):
    print(traceback.format_exc())
    if isinstance(e, HTTPException):
        return jsonify({
            "error": e.description,
            "code": e.code
        }), e.code

    return jsonify({
        "error": "Internal Server Error",
        "code": 500
    }), 500

@app.route("/")
def home():
    return "Turso + Flask is working!"
    

if __name__ == "__main__":
    app.run(debug=True)