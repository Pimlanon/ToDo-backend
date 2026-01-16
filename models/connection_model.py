from dataclasses import dataclass

@dataclass
class Connection:
    id: str
    page_id: str
    name: str
    email: str
