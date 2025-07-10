import pytest
from app.services.auth_service import AuthService
from unittest.mock import MagicMock, patch
from app.exceptions.custom_exceptions import ValidationException, UserException


class DummyDB:
    pass


def test_auth_service_instance():
    mock_db = MagicMock()
    service = AuthService(mock_db)
    assert service is not None


def test_authenticate_user_missing_email():
    mock_db = MagicMock()
    service = AuthService(mock_db)
    with pytest.raises(ValidationException):
        service.authenticate_user("", "password123")


def test_register_user_missing_username():
    mock_db = MagicMock()
    service = AuthService(mock_db)
    user_create = MagicMock()
    user_create.email = "test@example.com"
    user_create.password = "password123"
    user_create.username = ""
    with pytest.raises(ValidationException):
        service.register_user(user_create)


def test_register_user_existing_user():
    mock_db = MagicMock()
    service = AuthService(mock_db)
    user_create = MagicMock()
    user_create.email = "test@example.com"
    user_create.password = "password123"
    user_create.username = "testuser"
    with patch(
        "app.repositories.user_repository.UserRepository.get_by_email",
        return_value=True,
    ):
        with pytest.raises(UserException):
            service.register_user(user_create)
