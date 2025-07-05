from sqlalchemy.orm import Session
from app.repositories.article_repository import ArticleRepository
from app.schemas.article import ArticleCreate
from app.services.notification_service import NotificationService
from app.external.news_api import NewsAPIClient
from app.repositories.external_source_repository import ExternalSourceRepository
from app.models.external_source import ExternalSource
from app.tasks.category_classifier import CategoryClassifier
from app.repositories.category_repository import CategoryRepository
from app.models.notification import NotificationConfig, Notification
from app.repositories.notification_repository import NotificationRepository
from app.services.email_service import EmailService
from app.models import article


class NewsService:

    def __init__(self, db: Session):
        self.db = db
        self.notification_service = NotificationService(db)
        self.classifier = CategoryClassifier()

    def get_articles(self, skip: int = 0, limit: int = 10):
        return ArticleRepository.get_all(db=self.db, skip=skip, limit=limit)

    def get_article(self, article_id: int):
        return ArticleRepository.get_by_id(db=self.db, article_id=article_id)
    
    def trigger_notifications(self, articles: list):
        print("[DEBUG] Triggering notifications for new articles...")
        
        for article in articles:
            if not article.category:
                continue

            # Get all users who have this category enabled
            configs = self.db.query(NotificationConfig).filter_by(category=article.category, enabled=True).all()
            keyword_configs = self.db.query(NotificationConfig).filter(
                NotificationConfig.keyword.isnot(None),
                NotificationConfig.enabled.is_(True)
            ).all()

            notified_users = set()

            # Category-based notifications
            for config in configs:
                if config.user_id in notified_users:
                    continue
                message = f"New article in {article.category}: {article.title}"
                self._create_and_send_notification(config.user_id, message,article.url)
                notified_users.add(config.user_id)

            # Keyword-based notifications
            article_text = f"{article.title} {article.content or ''}".lower()
            for config in keyword_configs:
                if config.user_id in notified_users:
                    continue
                if config.keyword and config.keyword.lower() in article_text:
                    message = f"New article matching keyword '{config.keyword}': {article.title}"
                    self._create_and_send_notification(config.user_id, message)
                    notified_users.add(config.user_id)

    def _create_and_send_notification(self, user_id: int, message: str,url: str = None):
        NotificationRepository.create(self.db, user_id=user_id, message=message)

        email_service = EmailService(self.db)
        email_service.send_notification_email(user_id, message, url)


    def fetch_and_store_top_headlines(self, category: str = None):
        client = NewsAPIClient()
        headlines = client.fetch_top_headlines(category=category)

        new_articles = []

        for article_data in headlines:
            full_text = (
                (article_data.get("title") or "")
                + " "
                + (article_data.get("content") or "")
            )
            detected_category = self.classifier.classify(full_text)

            CategoryRepository.create_if_not_exists(self.db, detected_category)

            article = ArticleRepository.create(
                db=self.db,
                title=article_data["title"],
                content=article_data.get("content") or "",
                url=article_data.get("url") or None,
                category=detected_category,
            )
            new_articles.append(article)

        newsapi_source = self.db.query(ExternalSource).filter_by(name="newsAPI").first()
        if newsapi_source:
            ExternalSourceRepository.update_last_accessed(self.db, newsapi_source.id)

        self.trigger_notifications(new_articles)
