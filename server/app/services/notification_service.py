from app.repositories.notification_repository import NotificationRepository

class NotificationService:
    def __init__(self, db):
        self.db = db

    def get_user_configs(self, user_id: int):
        return NotificationRepository.get_by_user(self.db, user_id)

    def update_config(self, config_id: int, enabled: bool):
        return NotificationRepository.update(self.db, config_id, enabled)

    def update_keywords(self, user_id: int, keywords: list[str]):
        return NotificationRepository.set_keywords(self.db, user_id, keywords)
