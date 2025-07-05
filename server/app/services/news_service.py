from sqlalchemy.orm import Session
from app.repositories.article_repository import ArticleRepository
from app.schemas.article import ArticleCreate
from app.services.notification_service import NotificationService
from app.external.news_api import NewsAPIClient
from app.repositories.external_source_repository import ExternalSourceRepository
from app.models.external_source import ExternalSource
from app.tasks.category_classifier import CategoryClassifier
from app.repositories.category_repository import CategoryRepository


class NewsService:

    def __init__(self, db: Session):
        self.db = db
        self.notification_service = NotificationService(db)
        self.classifier = CategoryClassifier()

    def get_articles(self, skip: int = 0, limit: int = 10):
        return ArticleRepository.get_all(db=self.db, skip=skip, limit=limit)

    def get_article(self, article_id: int):
        return ArticleRepository.get_by_id(db=self.db, article_id=article_id)

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

        # self.trigger_notifications(new_articles)
