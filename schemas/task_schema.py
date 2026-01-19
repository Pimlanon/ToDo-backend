from pydantic import BaseModel
from typing import Optional

class TaskBase(BaseModel):
    page_id: str
    title: str
    status: int
    description: Optional[str] = None
    priority: Optional[int] = None
    due_date: Optional[str] = None
    connection_ids: Optional[list[str]] = []

    class Config:
        str_strip_whitespace = True # strip whitespace from all str fields

class TaskCreate(TaskBase):
    pass

class TaskUpdate(TaskBase):
    pass