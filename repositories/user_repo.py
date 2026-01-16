from db import get_db
from models.user_model import User

class UserRepository:
    
    def email_exists(self, email: str) -> bool:
        db = get_db()
        result = db.execute(
            "SELECT 1 FROM users WHERE email = ? LIMIT 1",
            [email]
        )
        return bool(result.rows)

    def create(self, user: User):
        db = get_db()
        db.execute("""
            INSERT INTO users (id, username, password, email, created_at)
            VALUES (?, ?, ?, ?, ?)
        """, [user.id, user.username, user.password, user.email, user.created_at])


    def find_all(self):
        db = get_db()
        result = db.execute("SELECT * FROM users")
        columns = result.columns
        return [
            User(**dict(zip(columns, row)))
            for row in result.rows
        ]

    def find_by_id(self, user_id: str):
        db = get_db()
        result = db.execute("SELECT * FROM users WHERE id = ?", [user_id])
        if not result.rows:
            return None

        row = result.rows[0]
        columns = result.columns
        data = dict(zip(columns, row))

        return User(**data)

    def delete(self, user_id: str):
        db = get_db()
        db.execute("DELETE FROM users WHERE id = ?", [user_id])
       
