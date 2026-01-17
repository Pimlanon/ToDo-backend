from db import get_db
from models.page_model import Page

class PageRepository:

    def create(self, page: Page ):
        db = get_db()
        db.execute("""
            INSERT INTO pages (id,  user_id, title, created_at)
            VALUES (?, ?, ?, ?)
        """, [page.id, page.user_id, page.title, page.created_at])

    def find_by_page_user(self, page_id: str, user_id :str):
        db = get_db()
        result = db.execute(""" 
            SELECT 
                t.id,
                t.title,
                t.status,
                t.position,
                t.description,
                t.priority,
                t.due_date,
                t.created_at,
                c.id    AS connection_id,
                c.name   AS connection_name,
                c.email  AS connection_email
            FROM tasks t
            JOIN pages p 
                ON t.page_id = p.id
            LEFT JOIN task_connections tc
                ON t.id = tc.task_id
            LEFT JOIN connections c
                ON tc.connection_id = c.id
            WHERE t.page_id = ?
            AND p.user_id = ?;
        """, [page_id, user_id])

        columns = result.columns
        rows = result.rows

        tasks = []
        for row in rows:
            data = dict(zip(columns, row))
            tasks.append(data)
        return tasks

    