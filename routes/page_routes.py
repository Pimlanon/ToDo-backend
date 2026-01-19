from flask import Blueprint, request, jsonify
from services.page_service import PageService
from schemas.page_schema import PageUpdate

page_bp = Blueprint("pages", __name__)
service = PageService()

@page_bp.post("")
def create_pages():
    page = service.create_page()
    return jsonify(page.to_dict()), 201


@page_bp.get("/<page_id>/tasks")
def get_page_tasks(page_id):
    tasks = service.get_tasks_with_connections(page_id)

    return jsonify({
        "page_id": page_id,
        "tasks": tasks
    })

@page_bp.get("")
def get_pages():
    pages = service.get_all()
    return jsonify(pages)

@page_bp.put("/<page_id>/title")
def update_page_title(page_id):
    payload = PageUpdate.model_validate(request.json)
    service.update_title(page_id, payload.title)

    return jsonify({"message": "Title updated"})