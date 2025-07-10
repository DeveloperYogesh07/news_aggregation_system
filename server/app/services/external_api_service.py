from sqlalchemy.orm import Session
from app.external.news_api import NewsAPIClient
from app.repositories.external_source_repository import ExternalSourceRepository
from app.models.external_source import ExternalSource
from typing import Optional, List, Dict
from app.exceptions.custom_exceptions import ExternalAPIException


class ExternalAPIService:
    """Service responsible for external API operations only."""

    def __init__(self, db: Session):
        self.db = db
        self.client = NewsAPIClient()

    def fetch_headlines(self, category: Optional[str] = None) -> List[Dict]:
        try:
            headlines = self.client.fetch_top_headlines(category=category)
            self._update_last_accessed()
            return headlines
        except Exception as e:
            raise ExternalAPIException(
                f"Failed to fetch headlines: {str(e)}",
                api_name="NewsAPI",
                status_code=500,
            )

    def _update_last_accessed(self):
        try:
            newsapi_source = (
                self.db.query(ExternalSource).filter_by(name="newsAPI").first()
            )
            if newsapi_source:
                ExternalSourceRepository.update_last_accessed(self.db, newsapi_source.id)  # type: ignore
        except Exception as e:
            pass
