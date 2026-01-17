from flask import Blueprint, request, jsonify
from services.connection_service import ConnectionService
from schemas.connection_schema import ConnectionCreate

connection_bp = Blueprint("connections", __name__)
service = ConnectionService()

@connection_bp.post("")
def create_connection():
    payload = ConnectionCreate.model_validate(request.json)
    connection = service.create_connection(payload)
    return jsonify(connection.to_dict()), 201

@connection_bp.get("/<id>")
def get_connections(id):
    connections = service.get_connections(id)
    return jsonify(connections), 200

@connection_bp.delete("/<id>")
def delete_connection(id):
    service.delete_connection(id)
    return jsonify({"message": "connection deleted successfully"})