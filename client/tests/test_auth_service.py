import pytest
from client.services.auth_service import AuthenticationService
from client.services.api_client import APIClient
from client.exceptions.custom_exceptions import AuthenticationError, NetworkError


def test_auth_service_instance():
    api_client = APIClient()
    service = AuthenticationService(api_client)
    assert service is not None


def test_signup_invalid_username():
    api_client = APIClient()
    service = AuthenticationService(api_client)
    result = service.signup("ab", "test@example.com", "password123")
    assert result is None


def test_login_invalid_email():
    api_client = APIClient()
    service = AuthenticationService(api_client)
    result = service.login("invalid-email", "password123")
    assert result is None


def test_signup_invalid_email():
    api_client = APIClient()
    service = AuthenticationService(api_client)
    result = service.signup("validuser", "invalid-email", "password123")
    assert result is None


def test_signup_invalid_password():
    api_client = APIClient()
    service = AuthenticationService(api_client)
    result = service.signup("validuser", "test@example.com", "pw")
    assert result is None
