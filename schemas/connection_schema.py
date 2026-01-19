from pydantic import BaseModel, EmailStr

class ConnectionBase(BaseModel):
    page_id: str
    name: str
    email: EmailStr
    color: str

class ConnectionCreate(ConnectionBase):
    pass