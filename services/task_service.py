from repositories.task_repo import TaskRepository
from schemas.task_schema import TaskCreate
from models.task_model import Task
from repositories.relation_repo import RelationRepository
import uuid
from datetime import datetime

repo = TaskRepository()
relation_repo = RelationRepository()

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
    
    def get_tasks(self):
        return repo.find_all()
    
    def delete_task(self, task_id):
        # check if task exist
        task = repo.find_by_id(task_id)
        if not task:
            return None

        relation_repo.delete_by_task(task_id)
        repo.delete(task_id)
        return task