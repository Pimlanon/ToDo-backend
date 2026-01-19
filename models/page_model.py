from dataclasses import dataclass

@dataclass
class Page:
    id: str
    title: str
    created_at: str

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "created_at": self.created_at
        }