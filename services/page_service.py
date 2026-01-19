from repositories.page_repo import PageRepository
from models.page_model import Page
import uuid
from datetime import datetime
import json
from pathlib import Path
from datetime import datetime, timezone

repo = PageRepository()

class PageService:

    def create_page(self, user_id: str):
        page = Page(
            id=str(uuid.uuid4()),
            user_id=user_id,
            title="Edit Your Board's Name Here !",
            created_at=datetime.utcnow().isoformat(),
        )
        repo.create(page)
        return page
    
    def update_title(self, page_id: str, title: str):
        return repo.update_title(page_id, title)
    
    def get_all_by_user(self, user_id :str):
        pages = repo.find_all_by_user(user_id)
        return {
            "count": len(pages),
            "items": [p.to_dict() for p in pages]
        }
    
    def is_overdue(self, task, today):
        if not task.get("due_date"):
            return False
        due = datetime.fromisoformat(task["due_date"].replace("Z", "+00:00"))
        return (today > due) and (task["status"] != 3) # not include 'done' 

    def get_tasks_with_connections(self, page_id: str, user_id: str):

        BASE_DIR = Path(__file__).resolve().parent.parent  # location: parent-folder/
        JSON_PATH = BASE_DIR / "data" / "tasks.json" # parent-folder/data/tasks.json
      
        # load json
        with open(JSON_PATH, "r", encoding="utf-8") as f:
            json_tasks = json.load(f)

        # setup tasks
        tasks = {}

        # put json data to tasks 
        for t in json_tasks:
            tasks[t["id"]] = {
                **t,
                "connections": []
            }

        # ---- data from DB ---
        rows = repo.find_by_page_user(page_id, user_id)
        for row in rows:
            task_id = row["id"]

            if task_id not in tasks:
                tasks[task_id] = {
                    "id": row["id"],
                    "title": row["title"],
                    "status": row["status"],
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
                    "email": row["connection_email"],
                    "color": row["connection_color"]
                })
        
        # prepare status + set today
        map_status = {
            "todo": [],
            "in_progress": [],
            "done": []
        }
        today = datetime.now(timezone.utc) 

        # group by status + overdue
        for task in tasks.values():

            # check overdue task
            task["over_due"] = self.is_overdue(task, today)

            # separate by status + merge to same 'map_status'
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

        