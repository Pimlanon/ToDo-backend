from pydantic import BaseModel
from typing import Optional

class TaskBase(BaseModel):
    page_id: str
    title: str
    status: int
    position: int 
    description: Optional[str] = None
    priority: Optional[int] = None
    due_date: Optional[str] = None

    class Config:
        anystr_strip_whitespcae = True # strip whitespace from all str fields

class TaskCreate(TaskBase):
    pass

class TaskUpdate(TaskBase):
    pass