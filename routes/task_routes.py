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