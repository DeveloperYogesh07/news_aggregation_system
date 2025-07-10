from sqlalchemy.orm import Session
from app.repositories.external_source_repository import ExternalSourceRepository


class ExternalSourceService:
    def __init__(self, db: Session):
        self.db = db

    def create(self, data):
        return ExternalSourceRepository.create(self.db, **data.model_dump())

    def list_sources(self):
        return ExternalSourceRepository.get_all(self.db)

    def delete(self, source_id: int):
        source = ExternalSourceRepository.get_by_id(self.db, source_id)
        if source:
            ExternalSourceRepository.delete(self.db, source)
        return source

    def update(self, source_id: int, data):
        source = ExternalSourceRepository.get_by_id(self.db, source_id)
        if not source:
            return None
        return ExternalSourceRepository.update(
            self.db, source, **data.model_dump(exclude_unset=True)
        )
