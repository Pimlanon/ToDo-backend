from pydantic import BaseModel, EmailStr

class UserBase(BaseModel):
    username: str
    password: str
    email: EmailStr

class UserCreate(UserBase):
    pass