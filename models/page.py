from dataclasses import dataclass

@dataclass
class Page:
    id: str
    user_id: str
    title: str
    created_at: str