import pytest
from app.services.notification_service import NotificationService
from unittest.mock import MagicMock


def test_notification_service_instance():
    mock_db = MagicMock()
    service = NotificationService(mock_db)
    assert service is not None
