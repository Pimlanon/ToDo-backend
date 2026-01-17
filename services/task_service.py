from repositories.task_repo import TaskRepository
from schemas.task_schema import TaskCreate
from models.task_model import Task
import uuid
from datetime import datetime

repo = TaskRepository()

class TaskService:

    def create_task(self, data: TaskCreate):
        task = Task(
            id=str(uuid.uuid4()),
            page_id=data.page_id,
            title=data.title,
            status=data.status,
            position=data.position,
            created_at=datetime.utcnow().isoformat(),
            description=data.description,
            priority=data.priority,
            due_date=data.due_date,
        )
        repo.create(task)
        return task