from db import get_db

class RelationRepository: 
    def delete_by_task(self, task_id: str):
            db = get_db()
            db.execute("DELETE FROM task_connections WHERE task_id = ?", [task_id])
