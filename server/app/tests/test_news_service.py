import pytest
from app.services.news_service import NewsService
from unittest.mock import MagicMock, patch
from app.exceptions.custom_exceptions import ArticleException


class DummyDB:
    pass


def test_news_service_instance():
    mock_db = MagicMock()
    service = NewsService(mock_db)
    assert service is not None


def test_get_articles_calls_repository():
    mock_db = MagicMock()
    service = NewsService(mock_db)
    with patch(
        "app.repositories.article_repository.ArticleRepository.get_all", return_value=[]
    ) as mock_get_all:
        articles = service.get_articles()
        mock_get_all.assert_called_once()
        assert articles == []


def test_get_article_not_found():
    mock_db = MagicMock()
    service = NewsService(mock_db)
    with patch(
        "app.repositories.article_repository.ArticleRepository.get_by_id",
        return_value=None,
    ):
        with pytest.raises(ArticleException):
            service.get_article(123)


def test_fetch_and_store_top_headlines():
    mock_db = MagicMock()
    service = NewsService(mock_db)
    with patch.object(
        service.external_api, "fetch_headlines", return_value=["headline1", "headline2"]
    ) as mock_fetch, patch.object(
        service.article_processing,
        "process_and_store_articles",
        return_value=["article1", "article2"],
    ) as mock_process:
        result = service.fetch_and_store_top_headlines("tech")
        mock_fetch.assert_called_once_with("tech")
        mock_process.assert_called_once_with(["headline1", "headline2"])
        assert result == ["article1", "article2"]
