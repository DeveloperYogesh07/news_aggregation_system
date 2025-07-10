from sqlalchemy.orm import Session
from app.repositories.article_repository import ArticleRepository
from app.repositories.category_repository import CategoryRepository
from app.services.notification_service import NotificationService
from app.tasks.category_classifier import CategoryClassifier
from app.models.notification import NotificationConfig
from app.repositories.notification_repository import NotificationRepository
from app.services.email_service import EmailService
from typing import List, Dict, Optional
from app.exceptions.custom_exceptions import ArticleException, NotificationException


class ArticleProcessingService:
    """Service responsible for article processing and notification triggering."""

    def __init__(self, db: Session):
        self.db = db
        self.classifier = CategoryClassifier()
        self.notification_service = NotificationService(db)

    def process_and_store_articles(self, headlines: List[Dict]) -> List:
        try:
            new_articles = []
            for article_data in headlines:
                article = self._process_single_article(article_data)
                new_articles.append(article)

            self._trigger_notifications(new_articles)
            return new_articles
        except Exception as e:
            raise ArticleException(
                f"Failed to process articles: {str(e)}", operation="process_and_store"
            )

    def _process_single_article(self, article_data: Dict):
        try:
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
            return article
        except Exception as e:
            raise ArticleException(
                f"Failed to process article: {str(e)}", operation="process_single"
            )

    def _trigger_notifications(self, articles: List):
        try:
            for article in articles:
                if not article.category:
                    continue

                self._process_category_notifications(article)
                self._process_keyword_notifications(article)
        except Exception as e:
            raise NotificationException(
                f"Failed to trigger notifications: {str(e)}",
                notification_type="article",
            )

    def _process_category_notifications(self, article):
        try:
            configs = (
                self.db.query(NotificationConfig)
                .filter_by(category=article.category, enabled=True)
                .all()
            )

            notified_users = set()
            for config in configs:
                if config.user_id in notified_users:  # type: ignore
                    continue
                message = f"New article in {article.category}: {article.title}"
                self._create_and_send_notification(config.user_id, message, article.url)  # type: ignore
                notified_users.add(config.user_id)  # type: ignore
        except Exception as e:
            raise NotificationException(
                f"Failed to process category notifications: {str(e)}",
                notification_type="category",
            )

    def _process_keyword_notifications(self, article):
        try:
            keyword_configs = (
                self.db.query(NotificationConfig)
                .filter(
                    NotificationConfig.keyword.isnot(None),
                    NotificationConfig.enabled.is_(True),
                )
                .all()
            )

            notified_users = set()
            article_text = f"{article.title} {article.content or ''}".lower()

            for config in keyword_configs:
                if config.user_id in notified_users:  # type: ignore
                    continue
                if config.keyword and config.keyword.lower() in article_text:  # type: ignore
                    message = f"New article matching keyword '{config.keyword}': {article.title}"  # type: ignore
                    self._create_and_send_notification(config.user_id, message)  # type: ignore
                    notified_users.add(config.user_id)  # type: ignore
        except Exception as e:
            raise NotificationException(
                f"Failed to process keyword notifications: {str(e)}",
                notification_type="keyword",
            )

    def _create_and_send_notification(
        self, user_id: int, message: str, url: Optional[str] = None
    ):
        try:
            NotificationRepository.create(self.db, user_id=user_id, message=message)
            email_service = EmailService(self.db)
            email_service.send_notification_email(user_id, message, url)
        except Exception as e:
            raise NotificationException(
                f"Failed to create notification: {str(e)}", user_id=user_id
            )
