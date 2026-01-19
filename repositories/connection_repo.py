from db import get_db
from models.connection_model import Connection

class ConnectionRepository:

    def create(self, connection: Connection):
        db = get_db()
        db.execute("""
            INSERT INTO connections (id, page_id, name, email, color, created_at)
            VALUES (?, ?, ?, ?, ?, ?)
        """, [connection.id, connection.page_id, connection.name, connection.email, connection.color, connection.created_at])

    def exists_by_page_and_email(self, page_id: str, email: str) -> bool:
        db = get_db()
        result = db.execute("""
            SELECT 1 FROM connections
            WHERE page_id = ? AND email = ?
            LIMIT 1
        """, [page_id, email])

        return bool(result.rows)
    
    def find_by_page(self, page_id: str):
        db = get_db()
        result = db.execute("""
            SELECT * FROM connections
            WHERE page_id = ?
            ORDER BY name COLLATE NOCASE ASC;
        """, [page_id])
        columns = result.columns
        connections = []

        for row in result.rows:
            data = dict(zip(columns, row))
            connections.append(Connection(**data))

        return connections
    
    def find_by_id(self, connection_id: str):
        db = get_db()
        result = db.execute("SELECT * FROM connections WHERE id = ?", [connection_id])
        if not result.rows:
            return None

        row = result.rows[0]
        columns = result.columns
        data = dict(zip(columns, row))

        return Connection(**data)
    
    def delete(self, connection_id: str):
        db = get_db()
        db.execute("DELETE FROM connections WHERE id = ?", [connection_id])