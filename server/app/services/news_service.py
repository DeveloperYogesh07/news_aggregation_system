from sqlalchemy.orm import Session
from app.repositories.article_repository import ArticleRepository
from app.schemas.article import ArticleCreate
from app.services.notification_service import NotificationService
from app.external.news_api import NewsAPIClient
from app.repositories.external_source_repository import ExternalSourceRepository
from app.models.external_source import ExternalSource


class NewsService:

    def __init__(self, db: Session):
        self.db = db
        self.notification_service = NotificationService(db)

    def get_articles(self, skip: int = 0, limit: int = 10):
        return ArticleRepository.get_all(db=self.db, skip=skip, limit=limit)

    def get_article(self, article_id: int):
        return ArticleRepository.get_by_id(db=self.db, article_id=article_id)

    def fetch_and_store_top_headlines(self, category: str = None):
        client = NewsAPIClient()
        headlines = client.fetch_top_headlines(category=category)

        for article_data in headlines:
            ArticleRepository.create(
                db=self.db,
                title=article_data["title"],
                content=article_data["content"] or "",
            )

        newsapi_source = self.db.query(ExternalSource).filter_by(name="newsAPI").first()
        if newsapi_source:
            ExternalSourceRepository.update_last_accessed(self.db, newsapi_source.id)
