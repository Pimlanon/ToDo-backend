from dataclasses import dataclass

@dataclass
class Tag:
    id: str
    page_id: str
    name: str
    color: str
