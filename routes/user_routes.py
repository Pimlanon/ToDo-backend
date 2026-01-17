from flask import Blueprint, request, jsonify
from services.user_service import UserService
from schemas.user_schema import UserCreate

user_bp = Blueprint("users", __name__)
service = UserService()

@user_bp.post("")
def create_user():
    payload = UserCreate.model_validate(request.json)
    user = service.create_user(payload)
    return jsonify(user.to_dict()), 201

@user_bp.get("")
def get_users():
    print("Reached /api/users endpoint")
    users = service.get_users()
    return jsonify([u.to_dict() for u in users])

@user_bp.get("/<string:id>")
def get_user(id):
    user = service.get_user(id)
    return jsonify(user.to_dict())

@user_bp.delete("/<id>")
def delete_user(id):
    service.delete_user(id)
    return jsonify({"message": "User deleted successfully"})
