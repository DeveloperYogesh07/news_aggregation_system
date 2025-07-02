from sqlalchemy.orm import Session
from app.models.external_source import ExternalSource
from datetime import datetime

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

    @staticmethod
    def update(db: Session, source: ExternalSource, **kwargs):
        for key, value in kwargs.items():
            if value is not None:
                setattr(source, key, value)
        db.commit()
        db.refresh(source)
        return source
    

    @staticmethod
    def update_last_accessed(db: Session, source_id: int):
        from datetime import datetime
        source = db.query(ExternalSource).filter_by(id=source_id).first()
        if source:
            source.last_accessed = datetime.utcnow()
            db.commit()
            db.refresh(source)
            print(f"[DEBUG] last_accessed updated for source ID {source_id}")  # ✅ Log here
        else:
            print(f"[DEBUG] Source ID {source_id} not found")

