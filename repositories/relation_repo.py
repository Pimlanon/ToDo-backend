from db import get_db

class RelationRepository: 
    def delete_by_task(self, task_id: str):
        db = get_db()
        db.execute("DELETE FROM task_connections WHERE task_id = ?", [task_id])

    def delete_by_connection(self, connection_id: str):
        db = get_db()
        db.execute("DELETE FROM task_connections WHERE connection_id = ?", [connection_id])

    def delete(self, task_id: str, connection_id: str):
        db = get_db()
        db.execute("""
             DELETE FROM task_connections
             WHERE task_id = ? AND connection_id = ?
        """, [task_id, connection_id])

    def find_by_task_id(self, task_id: str):
        db = get_db()
        rows = db.execute("""
             SELECT connection_id FROM task_connections WHERE task_id = ?
             """, [task_id])
        return [r["connection_id"] for r in rows]
        
    def create(self, task_id: str, connection_id: str):
        db = get_db()
        db.execute("""
            INSERT INTO task_connections (task_id, connection_id)
            VALUES (?, ?)
         """, [task_id, connection_id])
