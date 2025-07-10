import pytest
from app.services.external_source_service import ExternalSourceService
from unittest.mock import MagicMock


def test_external_source_service_instance():
    mock_db = MagicMock()
    service = ExternalSourceService(mock_db)
    assert service is not None
