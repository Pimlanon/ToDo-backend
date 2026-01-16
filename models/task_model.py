from dataclasses import dataclass
from typing import Optional

@dataclass
class Task:
    id: str
    page_id: str
    title: str
    description: Optional[str]
    priority: Optional[int]  # contain → 1:urgent, 2:normal, 3:low
    due_date: Optional[str]
    status: int  # contain → 1:todo, 2:in_progress, 3:done
    position: int
    created_at: str
