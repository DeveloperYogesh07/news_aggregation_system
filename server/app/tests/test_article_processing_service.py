import pytest
from app.services.article_processing_service import ArticleProcessingService
from unittest.mock import MagicMock


def test_article_processing_service_instance():
    mock_db = MagicMock()
    service = ArticleProcessingService(mock_db)
    assert service is not None
