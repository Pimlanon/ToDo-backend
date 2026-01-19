from flask import Blueprint, request, jsonify
from services.task_service import TaskService
from schemas.task_schema import TaskCreate, TaskUpdate

task_bp = Blueprint("tasks", __name__)
service = TaskService()

@task_bp.post("")
def create_task():
    payload = TaskCreate.model_validate(request.json)
    task = service.create_task(payload)
    return jsonify(task.to_dict()), 201

@task_bp.put("/<task_id>")
def update_task(task_id):
    payload = TaskUpdate.model_validate(request.json)
    task = service.update_task(task_id, payload)
    return jsonify(task.to_dict())

@task_bp.get("")
def get_tasks():
    tasks = service.get_tasks()
    return jsonify([t.to_dict() for t in tasks])

@task_bp.get("/sidebar/<page_id>")
def get_today_overdue_tasks(page_id):
    tasks = service.get_today_overdue_tasks(page_id)
    return jsonify(tasks)

@task_bp.delete("/<id>")
def delete_task(id):
    service.delete_task(id)
    return jsonify({"message": "Task deleted successfully"}), 200