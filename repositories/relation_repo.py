from db import get_db

class RelationRepository: 
    def delete_by_task(self, task_id: str):
            db = get_db()
            db.execute("DELETE FROM task_connections WHERE task_id = ?", [task_id])

    def delete_by_connection(self, connection_id: str):
            db = get_db()
            db.execute("DELETE FROM task_connections WHERE connection_id = ?", [connection_id])
