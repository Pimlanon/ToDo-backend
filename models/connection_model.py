from dataclasses import dataclass

@dataclass
class Connection:
    id: str
    page_id: str
    name: str
    email: str
    color: str
    created_at: str

    def to_dict(self):
        return {
            "id": self.id,
            "page_id": self.page_id,
            "name": self.name,
            "email": self.email,
            "color": self.color,
            "created_at": self.created_at
        }
