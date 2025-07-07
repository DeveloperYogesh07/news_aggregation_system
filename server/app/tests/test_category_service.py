import pytest
from app.services.category_service import CategoryService
from unittest.mock import MagicMock


def test_category_service_instance():
    mock_db = MagicMock()
    service = CategoryService(mock_db)
    assert service is not None
