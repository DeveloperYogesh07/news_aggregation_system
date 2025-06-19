from sqlalchemy.orm import Session
from app.repositories.notification_repository import NotificationRepository

class NotificationService:

    def __init__(self, db: Session):
        self.db = db

    def create_notification(self, user_id: int, message: str):
        return NotificationRepository.create(self.db, user_id, message)

    def get_notifications_for_user(self, user_id: int):
        return NotificationRepository.get_for_user(self.db, user_id)
