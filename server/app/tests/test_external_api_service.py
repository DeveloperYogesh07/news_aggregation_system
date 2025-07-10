import pytest
from app.services.external_api_service import ExternalAPIService
from unittest.mock import MagicMock


def test_external_api_service_instance():
    mock_db = MagicMock()
    service = ExternalAPIService(mock_db)
    assert service is not None
