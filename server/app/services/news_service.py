import logging
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
        self.logger = logging.getLogger(__name__)

    def get_articles(self, skip: int = 0, limit: int = 10):
        try:
            self.logger.debug(f"Fetching articles with skip={skip}, limit={limit}")
            articles = ArticleRepository.get_all(self.db, skip=skip, limit=limit)
            self.logger.debug(f"Retrieved {len(articles)} articles")
            return articles
        except Exception as e:
            self.logger.error(f"Failed to retrieve articles: {e}")
            raise ArticleException(
                f"Failed to retrieve articles: {str(e)}", operation="get_all"
            )

    def get_article(self, article_id: int):
        try:
            self.logger.debug(f"Fetching article with ID: {article_id}")
            article = ArticleRepository.get_by_id(db=self.db, article_id=article_id)
            if not article:
                self.logger.warning(f"Article with ID {article_id} not found")
                raise ArticleException(
                    f"Article with ID {article_id} not found",
                    article_id=article_id,
                    operation="get_by_id",
                )
            self.logger.debug(f"Retrieved article: {article.title}")
            return article
        except ArticleException:
            raise
        except Exception as e:
            self.logger.error(f"Failed to retrieve article {article_id}: {e}")
            raise ArticleException(
                f"Failed to retrieve article {article_id}: {str(e)}",
                article_id=article_id,
                operation="get_by_id",
            )

    def fetch_and_store_top_headlines(self, category: Optional[str] = None):
        try:
            self.logger.info(
                f"Fetching headlines for category: {category or 'general'}"
            )
            headlines = self.external_api.fetch_headlines(category)
            self.logger.info(f"Fetched {len(headlines)} headlines")

            new_articles = self.article_processing.process_and_store_articles(headlines)
            self.logger.info(f"Stored {len(new_articles)} new articles")
            return new_articles
        except ExternalAPIException:
            raise
        except Exception as e:
            self.logger.error(f"Failed to fetch and store headlines: {e}")
            raise ArticleException(
                f"Failed to fetch and store headlines: {str(e)}",
                operation="fetch_and_store",
            )
