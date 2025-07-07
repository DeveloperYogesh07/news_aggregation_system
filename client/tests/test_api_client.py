import pytest
from client.services.api_client import APIClient
from unittest.mock import patch


def test_api_client_instance():
    client_instance = APIClient()
    assert client_instance is not None


def test_set_token():
    client = APIClient()
    client.set_token("abc123")
    assert client.token == "abc123"


def test_clear_token():
    client = APIClient()
    client.set_token("abc123")
    client.clear_token()
    assert client.token is None


def test_build_url():
    client = APIClient(base_url="http://localhost")
    assert client._build_url("/test") == "http://localhost/test"
    assert client._build_url("test") == "http://localhost/test"


def test_set_token_empty():
    client = APIClient()
    with pytest.raises(ValueError):
        client.set_token("")


def test_get_categories_calls_get():
    client = APIClient()
    with patch.object(client, "get", return_value={"categories": []}) as mock_get:
        result = client.get_categories()
        mock_get.assert_called_once_with("/categories")
        assert result == {"categories": []}
