from sqlalchemy.orm import Session
from app.models.notification import Notification

class NotificationRepository:

    @staticmethod
    def create(db: Session, user_id: int, message: str):
        db_notification = Notification(user_id=user_id, message=message)
        db.add(db_notification)
        db.commit()
        db.refresh(db_notification)
        return db_notification

    @staticmethod
    def get_for_user(db: Session, user_id: int):
        return db.query(Notification).filter(Notification.user_id == user_id).all()
