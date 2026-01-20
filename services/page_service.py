from repositories.page_repo import PageRepository
from models.page_model import Page
import uuid
import json
from pathlib import Path
from datetime import datetime, timezone
from config import TH_TZ

repo = PageRepository()

class PageService:

    STATUS_MAP = {
        1: "todo",
        2: "in_progress", 
        3: "done"
    }

    def create_page(self):
        page = Page(
            id=str(uuid.uuid4()),
            title="Edit Your Board's Name Here !",
            created_at=datetime.utcnow().isoformat(),
        )
        repo.create(page)
        return page
    
    def update_title(self, page_id: str, title: str):
        return repo.update_title(page_id, title)
    
    def get_all(self):
        pages = repo.find_all()
        return {
            "count": len(pages),
            "items": [p.to_dict() for p in pages]
        }
    
    def _is_overdue(self, task, today):
        if not task.get("due_date"):
            return False
        due_utc = datetime.fromisoformat(task["due_date"].replace("Z", "+00:00"))

        # convert to Thailand time
        due_local = due_utc.astimezone(TH_TZ).date()
        today_local = today.astimezone(TH_TZ).date()

        return (today_local  > due_local) and (task["status"] != 3) # not include 'done' 

    def _load_json_tasks(self) :
        BASE_DIR = Path(__file__).resolve().parent.parent  # location: parent-folder/
        JSON_PATH = BASE_DIR / "data" / "tasks.json" # parent-folder/data/tasks.json

        with open(JSON_PATH, "r", encoding="utf-8") as f:
            json_tasks = json.load(f)
        
        return {
            task["id"]: {**task, "connections": []} 
            for task in json_tasks
        }
    
    def _build_connection(self, row) :
        """ build connection obj from db """
        return {
            "id": row["connection_id"],
            "name": row["connection_name"],
            "email": row["connection_email"],
            "color": row["connection_color"]
        }
    
    def _merge_db_tasks(self, tasks, db_rows) -> None:
        """
        merge tasks with their connections
        return a dict in the form:
        {
            "<id_task>": {
                "id": "<id_task>",
                "title": str,
                ...
                "connections": [{...}]
            }
        }
        """
        for row in db_rows:
            task_id = row["id"]
            
            # create task if doesn't exist
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
            
            # add connection if exists
            if row["connection_id"]:
                tasks[task_id]["connections"].append(
                    self._build_connection(row)
                )

    def _group_by_status(self, tasks, today) :
        """ 
        group by status + mark overdue 
        return
             {
                "todo": [{...}],
                "in_progress": [...]},
                "done": [...]}
            } 
        """
        grouped = {status: [] for status in self.STATUS_MAP.values()}
        
        for task in tasks.values():
            task["over_due"] = self._is_overdue(task, today)
            
            status_key = self.STATUS_MAP.get(task["status"])
            if status_key:
                grouped[status_key].append(task)
        
        return grouped    
    
    def _format_result(self, grouped_tasks) :
        """
        return
             {
                "todo": {"count": int, "items": [...]},
                "in_progress": {"count": int, "items": [...]},
                "done": {"count": int, "items": [...]}
            }
        """
        return {
            status: {
                "count": len(tasks),
                "items": tasks
            }
            for status, tasks in grouped_tasks.items()
        }
    
    def get_tasks_with_connections(self, page_id: str) :
        # load and merge data sources
        tasks = self._load_json_tasks()
        db_rows = repo.find_by_page(page_id)
        self._merge_db_tasks(tasks, db_rows)
        
        # group and format
        today = datetime.now(timezone.utc)
        grouped_tasks = self._group_by_status(tasks, today)

        return self._format_result(grouped_tasks)


        