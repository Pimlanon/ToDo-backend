from flask import Blueprint, request, jsonify
from services.task_service import TaskService
from schemas.task_schema import TaskCreate

task_bp = Blueprint("tasks", __name__)
service = TaskService()

@task_bp.post("")
def create_task():
    payload = TaskCreate.model_validate(request.json)
    task = service.create_task(payload)
    return jsonify(task.to_dict()), 201

@task_bp.get("")
def get_tasks():
    tasks = service.get_tasks()
    return jsonify([t.to_dict() for t in tasks])

@task_bp.delete("/<id>")
def delete_task(id):
    task = service.delete_task(id)

    if not task:
        return jsonify({"message": "Task not found"}), 404

    return jsonify({"message": "Task deleted successfully"}), 200