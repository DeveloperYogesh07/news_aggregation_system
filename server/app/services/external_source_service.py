from sqlalchemy.orm import Session
from app.schemas.external_source import ExternalSourceCreate, ExternalSourceUpdate
from app.repositories.external_source_repository import ExternalSourceRepository

class ExternalSourceService:

    def __init__(self, db: Session):
        self.db = db

    def create(self, create_data: ExternalSourceCreate):
        return ExternalSourceRepository.create(self.db, **create_data.dict())

    def list_sources(self):
        return ExternalSourceRepository.get_all(self.db)

    def get(self, source_id: int):
        return ExternalSourceRepository.get_by_id(self.db, source_id)

    def delete(self, source_id: int):
        source = self.get(source_id)
        if source:
            ExternalSourceRepository.delete(self.db, source)
        return source
