import pytest
from app.services.email_service import EmailService
from unittest.mock import MagicMock


def test_email_service_instance():
    mock_db = MagicMock()
    service = EmailService(mock_db)
    assert service is not None
