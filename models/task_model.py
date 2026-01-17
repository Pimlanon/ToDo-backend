from dataclasses import dataclass
from typing import Optional

@dataclass
class Task:
    id: str
    page_id: str
    title: str
    status: int   # contain → 1:todo, 2:in_progress, 3:done
    position: int 
    created_at: str
    description: Optional[str] = None
    priority: Optional[int] = None  # contain → 1:urgent, 2:normal, 3:low
    due_date: Optional[str] = None

    def to_dict(self):
        return {
            "id": self.id,
            "page_id": self.page_id,
            "title": self.title,
            "description": self.description,
            "priority": self.priority,
            "due_date": self.due_date,
            "status": self.status,
            "position": self.position,
            "created_at": self.created_at
        }