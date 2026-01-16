from repositories.user_repo import UserRepository
from models.user_model import User
from datetime import datetime
from schemas.user_schema import UserCreate
from utilities.password import hash_password
import uuid

repo = UserRepository()

class UserService:

    def create_user(self, data: UserCreate):
        # check duplicate email
        if repo.email_exists(data.email):
            raise ValueError("Email already exists")
        
        # hash password
        hashed_password = hash_password(data.password)

        user = User(
            id=str(uuid.uuid4()),
            username=data.username,
            password=hashed_password,
            email=data.email,
            created_at=datetime.utcnow().isoformat()
        )
        repo.create(user)
        return user

    def get_users(self):
        return repo.find_all()

    def get_user(self, user_id):
        user = repo.find_by_id(user_id)
        return  user

    def delete_user(self, user_id):
        # check if user exist
        user = repo.find_by_id(user_id)
        if not user:
            return None

        repo.delete(user_id)
        return user
