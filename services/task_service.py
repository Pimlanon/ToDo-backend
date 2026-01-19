from repositories.task_repo import TaskRepository
from schemas.task_schema import TaskCreate, TaskUpdate
from models.task_model import Task
from repositories.relation_repo import RelationRepository
import uuid
from datetime import datetime
from errors import NotFoundError

repo = TaskRepository()
relation_repo = RelationRepository()

class TaskService:

    def create_task(self, data: TaskCreate):
        task = Task(
            id=str(uuid.uuid4()),
            page_id=data.page_id,
            title=data.title,
            status=data.status,
            created_at=datetime.utcnow().isoformat(),
            updated_at=datetime.utcnow().isoformat(),
            description=data.description,
            priority=data.priority,
            due_date=data.due_date,
        )
        # create task
        repo.create(task)

        # create relations with connection
        if data.connection_ids:
            for cid in data.connection_ids:
                relation_repo.create(task.id, cid)

        return task
    
    def update_task(self, task_id: str, data: TaskUpdate):
        # get exisitng data
        old_task = repo.find_by_id(task_id)

        task = Task(
            id=task_id,
            page_id=data.page_id,
            title=data.title,
            status=data.status,
            created_at=old_task.created_at,
            updated_at=datetime.utcnow().isoformat(),
            description=data.description,
            priority=data.priority,
            due_date=data.due_date,
        )
        repo.update(task)

        # -- connection --
        # existing id from db
        old_ids = set(relation_repo.find_by_task_id(task_id))
        # connection id from user
        new_ids = set(data.connection_ids or [])

        # find new id (insert new row)
        to_add = new_ids - old_ids
        # find remove id (delete in db)
        to_delete = old_ids - new_ids

        # create new connection
        for cid in to_add:
            relation_repo.create(task_id, cid)

        # delete non-existing extension
        for cid in to_delete:
            relation_repo.delete(task_id, cid)

        return task
    
    def get_tasks(self):
        return repo.find_all()
    
    def delete_task(self, task_id):
        # check if task exist
        task = repo.find_by_id(task_id)
        if not task:
            raise NotFoundError("Task not found")

        # delete relations by task_id
        relation_repo.delete_by_task(task_id)

        # delete task
        repo.delete(task_id)
        return task