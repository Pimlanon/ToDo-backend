from repositories.connection_repo import ConnectionRepository
from models.connection_model import Connection
from repositories.relation_repo import RelationRepository
import uuid
from datetime import datetime
from errors import ConflictError, NotFoundError

repo = ConnectionRepository()
relation_repo = RelationRepository()

class ConnectionService:

    def create_connection(self, data:Connection):
        if repo.exists_by_page_and_email(data.page_id, data.email):
            raise ConflictError("This email already exists in this page")

        connection = Connection(
            id=str(uuid.uuid4()),
            page_id=data.page_id,
            name=data.name,
            email=data.email,
            created_at=datetime.utcnow().isoformat()
        )
        repo.create(connection)
        return connection
    
    def get_connections(self, page_id: str):
        connections = repo.find_by_page(page_id)
        return {
            "count": len(connections),
            "items": [c.to_dict() for c in connections]
        }
    
    def delete_connection(self, connection_id):
        # check if connection exist
        connection = repo.find_by_id(connection_id)
        if not connection:
            raise NotFoundError("Connection not found")

        # delete relations by connection_id
        relation_repo.delete_by_connection(connection_id)

        # delete connection
        repo.delete(connection_id)
        return connection