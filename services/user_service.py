from repositories.user_repo import UserRepository
from models.user_model import User
from datetime import datetime
from schemas.user_schema import UserCreate
from services.page_service import PageService
from utilities.password import hash_password
from errors import ConflictError, InternalError, NotFoundError
import uuid

repo = UserRepository()
page_service = PageService()

class UserService:

    def create_user(self, data: UserCreate):
        # check duplicate email
        if repo.email_exists(data.email):
            raise ConflictError("Email already exists")
        
        user = User(
            id=str(uuid.uuid4()),
            username=data.username,
            password=hash_password(data.password), # hash password
            email=data.email,
            created_at=datetime.utcnow().isoformat()
        )

        # create user
        repo.create(user)

        try:
            # create default page for new user
            page_service.create_page(user.id)

            return user
        
        except Exception :
            raise InternalError("User created but default page creation failed")

    def get_users(self):
        return repo.find_all()

    def get_user(self, user_id):
        user = repo.find_by_id(user_id)
        if not user:
            raise NotFoundError("User not found")
        return  user

    def delete_user(self, user_id):
        # check if user exist
        user = repo.find_by_id(user_id)
        if not user:
            raise NotFoundError("User not found")

        repo.delete(user_id)
        return user
