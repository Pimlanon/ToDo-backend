from dataclasses import dataclass

@dataclass
class TaskConnection:
    task_id: str
    connection_id: str


@dataclass
class TaskTag:
    task_id: str
    tag_id: str
