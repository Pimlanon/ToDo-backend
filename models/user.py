from dataclasses import dataclass

@dataclass
class User:
    id: str
    username: str
    password: str 
    email: str
    created_at: str