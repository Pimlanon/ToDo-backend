from flask import Blueprint, request, jsonify
from services.page_service import PageService

page_bp = Blueprint("pages", __name__)
service = PageService()

@page_bp.get("/<page_id>/tasks")
def get_page_tasks(page_id):
    # todo read user_id from token

    tasks = service.get_tasks_with_connections(page_id, user_id = "14691f02-c666-4a69-9613-3e72397a1ddd")

    return jsonify({
        "page_id": page_id,
        "tasks": tasks
    })

@page_bp.get("")
def get_pages():
    # todo read user_id from token
    pages = service.get_all_by_user("14691f02-c666-4a69-9613-3e72397a1ddd")
    return jsonify(pages)