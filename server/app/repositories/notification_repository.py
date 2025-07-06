from app.models.notification import Notification, NotificationConfig
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime, timezone


class NotificationRepository:

    @staticmethod
    def get_for_user(db: Session, user_id: int) -> List[Notification]:
        return (
            db.query(Notification)
            .filter_by(user_id=user_id)
            .order_by(Notification.created_at.desc())
            .all()
        )

    @staticmethod
    def get_by_user(db: Session, user_id: int) -> List[NotificationConfig]:
        return db.query(NotificationConfig).filter_by(user_id=user_id).all()

    @staticmethod
    def update(db: Session, config_id: int, enabled: bool) -> NotificationConfig:
        config = db.query(NotificationConfig).filter_by(id=config_id).first()
        if config:
            config.enabled = enabled  # type: ignore
            db.commit()
            db.refresh(config)
        return config

    @staticmethod
    def set_keywords(db: Session, user_id: int, keywords: List[str]):
        db.query(NotificationConfig).filter_by(user_id=user_id).filter(
            NotificationConfig.keyword.isnot(None)
        ).delete()

        for kw in keywords:
            db.add(NotificationConfig(user_id=user_id, keyword=kw, enabled=True))
        db.commit()

    @staticmethod
    def create(db: Session, user_id: int, message: str):
        notice = Notification(
            user_id=user_id, message=message, created_at=datetime.now(timezone.utc)
        )
        db.add(notice)
        db.commit()
        db.refresh(notice)
        return notice
