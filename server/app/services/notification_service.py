from app.repositories.notification_repository import NotificationRepository
from app.models.category import Category
from app.models.notification import NotificationConfig

class NotificationService:
    def __init__(self, db):
        self.db = db

    def get_user_configs(self, user_id: int):
        configs = NotificationRepository.get_by_user(self.db, user_id)
        
        if not configs:
            all_categories = self.db.query(Category).all()
            for cat in all_categories:
                config = NotificationConfig(user_id=user_id, category=cat.name, enabled=False)
                self.db.add(config)
            keyword_config = NotificationConfig(user_id=user_id, keyword="*", enabled=False)
            self.db.add(keyword_config)
            self.db.commit()
            configs = NotificationRepository.get_by_user(self.db, user_id)
        
        return configs


    def update_config(self, config_id: int, enabled: bool):
        return NotificationRepository.update(self.db, config_id, enabled)

    def update_keywords(self, user_id: int, keywords: list[str]):
        return NotificationRepository.set_keywords(self.db, user_id, keywords)
