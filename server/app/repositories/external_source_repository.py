from sqlalchemy.orm import Session
from app.models.external_source import ExternalSource

class ExternalSourceRepository:

    @staticmethod
    def create(db: Session, **kwargs) -> ExternalSource:
        source = ExternalSource(**kwargs)
        db.add(source)
        db.commit()
        db.refresh(source)
        return source

    @staticmethod
    def get_all(db: Session):
        return db.query(ExternalSource).all()

    @staticmethod
    def get_by_id(db: Session, source_id: int):
        return db.query(ExternalSource).filter(ExternalSource.id == source_id).first()

    @staticmethod
    def delete(db: Session, source: ExternalSource):
        db.delete(source)
        db.commit()
