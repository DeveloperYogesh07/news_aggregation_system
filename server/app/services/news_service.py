from sqlalchemy.orm import Session
from app.repositories.article_repository import ArticleRepository
from app.services.notification_service import NotificationService
from app.services.external_api_service import ExternalAPIService
from app.services.article_processing_service import ArticleProcessingService
from app.repositories.category_repository import CategoryRepository
from app.models.notification import NotificationConfig
from app.repositories.notification_repository import NotificationRepository
from app.services.email_service import EmailService
from typing import Optional
from app.exceptions.custom_exceptions import ArticleException, ExternalAPIException


class NewsService:
    """Service responsible for news article operations only."""

    def __init__(self, db: Session):
        self.db = db
        self.article_processing = ArticleProcessingService(db)
        self.external_api = ExternalAPIService(db)

    def get_articles(self, skip: int = 0, limit: int = 10):
        try:
            return ArticleRepository.get_all(self.db, skip=skip, limit=limit)
        except Exception as e:
            raise ArticleException(
                f"Failed to retrieve articles: {str(e)}", operation="get_all"
            )

    def get_article(self, article_id: int):
        try:
            article = ArticleRepository.get_by_id(db=self.db, article_id=article_id)
            if not article:
                raise ArticleException(
                    f"Article with ID {article_id} not found",
                    article_id=article_id,
                    operation="get_by_id",
                )
            return article
        except ArticleException:
            raise
        except Exception as e:
            raise ArticleException(
                f"Failed to retrieve article {article_id}: {str(e)}",
                article_id=article_id,
                operation="get_by_id",
            )

    def fetch_and_store_top_headlines(self, category: Optional[str] = None):
        try:
            headlines = self.external_api.fetch_headlines(category)
            new_articles = self.article_processing.process_and_store_articles(headlines)
            return new_articles
        except ExternalAPIException:
            raise
        except Exception as e:
            raise ArticleException(
                f"Failed to fetch and store headlines: {str(e)}",
                operation="fetch_and_store",
            )
