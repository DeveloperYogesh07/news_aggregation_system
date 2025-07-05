import keyword
from app.models.notification import NotificationConfig
from sqlalchemy.orm import Session

class NotificationRepository:
    @staticmethod
    def get_by_user(db: Session, user_id: int):
        return db.query(NotificationConfig).filter_by(user_id=user_id).all()

    @staticmethod
    def update(db: Session, config_id: int, enabled: bool):
        config = db.query(NotificationConfig).filter_by(id=config_id).first()
        if config:
            config.enabled = enabled
            db.commit()
        return config

    @staticmethod
    def set_keywords(db: Session, user_id: int, keywords: list[str]):
        db.query(NotificationConfig).filter_by(user_id=user_id).filter(NotificationConfig.keyword != None).delete()
        for kw in keywords:
            db.add(NotificationConfig(user_id=user_id, keyword=kw, enabled=True))
        db.commit()
