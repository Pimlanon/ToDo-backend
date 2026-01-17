from repositories.page_repo import PageRepository
from models.page_model import Page
import uuid
from datetime import datetime

repo = PageRepository()

class PageService:

    def create_page(self, user_id: str):
        page = Page(
            id=str(uuid.uuid4()),
            user_id=user_id,
            title="My First Board",
            created_at=datetime.utcnow().isoformat(),
        )
        repo.create(page)
        return page

    def get_tasks_with_connections(self, page_id: str, user_id: str):
        rows = repo.find_by_page_user(page_id, user_id)

        tasks = {}

        for row in rows:
            task_id = row["id"]

            if task_id not in tasks:
                tasks[task_id] = {
                    "id": row["id"],
                    "title": row["title"],
                    "status": row["status"],
                    "position": row["position"],
                    "description": row["description"],
                    "priority": row["priority"],
                    "due_date": row["due_date"],
                    "created_at": row["created_at"],
                    "connections": []
                }

            # add connection if exist
            if row["connection_id"]:
                tasks[task_id]["connections"].append({
                    "id": row["connection_id"],
                    "name": row["connection_name"],
                    "email": row["connection_email"]
                })
            
        # separate by status 1:todo, 2:in_progress, 3:done
        map_status = {
            "todo": [],
            "in_progress": [],
            "done": []
        }

        for task in tasks.values():
            if task["status"] == 1:
                map_status["todo"].append(task)
            elif task["status"] == 2:
                map_status["in_progress"].append(task)
            elif task["status"] == 3:
                map_status["done"].append(task)
        
        # count tasks in each status
        result = {
            "todo": {
                "count": len(map_status["todo"]),
                "items": map_status["todo"]
            },
            "in_progress": {
                "count": len(map_status["in_progress"]),
                "items": map_status["in_progress"]
            },
            "done": {
                "count": len(map_status["done"]),
                "items": map_status["done"]
            }
        }

        return result

        