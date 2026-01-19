from db import get_db
from models.task_model import Task
from datetime import datetime, timezone

class TaskRepository: 

    def create(self, task: Task):
        db = get_db()
        db.execute("""
            INSERT INTO tasks (id, page_id, title, status, created_at, updated_at, description, priority, due_date)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, [task.id, task.page_id, task.title, task.status, task.created_at, task.updated_at, task.description, task.priority, task.due_date])
        return 'task'
    
    def update(self, task: Task):
        db = get_db()
        db.execute("""
            UPDATE tasks
            SET title = ?, status = ?, description = ?, priority = ?, due_date = ?, updated_at = ?
            WHERE id = ?
        """, [task.title, task.status, task.description, task.priority, task.due_date, task.updated_at, task.id])
        return task

    def find_all(self):
        db = get_db()
        result = db.execute("SELECT * FROM tasks")
        columns = result.columns
        tasks = []

        for row in result.rows:
            data = dict(zip(columns, row))
            tasks.append(Task(**data))

        return tasks

    def find_by_id(self, task_id: str):
        db = get_db()
        result = db.execute("SELECT * FROM tasks WHERE id = ?", [task_id])
        if not result.rows:
            return None

        row = result.rows[0]
        columns = result.columns
        data = dict(zip(columns, row))

        return Task(**data)
    
    def find_today_overdue_tasks(self, page_id: str):
        db = get_db()
        today = datetime.now(timezone.utc).date().isoformat()

        result = db.execute("""
            SELECT 
                id,
                title,
                status,
                due_date
            FROM tasks 
            WHERE page_id = ? 
            AND status IN (1, 2)
            AND due_date IS NOT NULL
            AND due_date <= ?
            ORDER BY due_date ASC, created_at DESC
        """, [page_id, today])

        columns = result.columns
        tasks = []

        for row in result.rows:
            data = dict(zip(columns, row))
            tasks.append(data)
        
        return tasks

    def delete(self, task_id: str):
        db = get_db()
        db.execute("DELETE FROM tasks WHERE id = ?", [task_id])