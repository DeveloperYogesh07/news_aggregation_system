import logging
from typing import Dict, Any, Optional, Union
import requests
from requests.exceptions import RequestException, HTTPError, Timeout, ConnectionError

from exceptions.custom_exceptions import (
    NetworkError,
    AuthenticationError,
    DataProcessingError,
)


class APIClient:
    def __init__(
        self, base_url: str = "http://127.0.0.1:8000/api/v1", timeout: int = 30
    ):
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self.token: Optional[str] = None
        self.logger = logging.getLogger(__name__)

        if not base_url:
            raise ValueError("Base URL cannot be empty")

    def set_token(self, token: str) -> None:
        if not token:
            raise ValueError("Token cannot be empty")
        self.token = token
        self.logger.debug("Authentication token set")

    def clear_token(self) -> None:
        self.token = None
        self.logger.debug("Authentication token cleared")

    def _build_url(self, endpoint: str) -> str:
        if not endpoint.startswith("/"):
            endpoint = "/" + endpoint
        return f"{self.base_url}{endpoint}"

    def _get_headers(self) -> Dict[str, str]:
        headers = {"Content-Type": "application/json"}
        if self.token:
            headers["Authorization"] = f"Bearer {self.token}"
        return headers

    def _handle_response(self, response: requests.Response) -> Dict[str, Any]:
        # Log response without sensitive data
        log_content = response.text[:200]
        if "access_token" in log_content:
            # Mask JWT tokens in logs
            import re
            log_content = re.sub(r'"access_token":"[^"]*"', '"access_token":"***MASKED***"', log_content)
        
        self.logger.debug(f"Response status: {response.status_code}, content: {log_content}")
        try:
            response.raise_for_status()
            return response.json()
        except HTTPError as e:
            if response.status_code in (401, 403):
                self.logger.warning(f"Authentication failed: {response.status_code}")
                raise AuthenticationError(
                    "login",
                    "Invalid email or password",
                    response.status_code,
                )
            elif response.status_code >= 500:
                self.logger.error(f"Server error {response.status_code}: {response.text}")
                raise DataProcessingError(
                    "server",
                    "Server error occurred",
                    f"HTTP {response.status_code}",
                )
            else:
                self.logger.error(f"HTTP error {response.status_code}: {response.text}")
                raise NetworkError(
                    "API request",
                    f"Request failed with status {response.status_code}",
                    self._build_url(""),
                )
        except ValueError as e:
            self.logger.error(f"Invalid JSON response: {e}")
            raise DataProcessingError(
                "data processing", "Server returned invalid data", "API response"
            )

    def _make_request(
        self,
        method: str,
        endpoint: str,
        data: Optional[Dict[str, Any]] = None,
        params: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        url = self._build_url(endpoint)
        headers = self._get_headers()

        try:
            self.logger.debug(f"Making {method} request to {url}")

            response = requests.request(
                method=method,
                url=url,
                json=data,
                params=params,
                headers=headers,
                timeout=self.timeout,
            )

            return self._handle_response(response)

        except Timeout:
            self.logger.error(f"Request timeout for {url}")
            raise NetworkError(
                "connection", "Request timed out. Please try again.", url
            )
        except ConnectionError:
            self.logger.error(f"Connection error for {url}")
            raise NetworkError(
                "connection",
                "Unable to connect to server. Please check your connection.",
                url,
            )
        except RequestException as e:
            self.logger.error(f"Request failed for {url}: {e}")
            raise NetworkError(
                "connection", "Connection failed. Please try again.", url
            )
        except (AuthenticationError, NetworkError, DataProcessingError):
            # Re-raise these specific exceptions without wrapping them
            raise
        except Exception as e:
            self.logger.error(f"Unexpected error for {url}: {e}")
            raise DataProcessingError(
                "request",
                "An unexpected error occurred. Please try again.",
                "API request",
            )

    def get(
        self, endpoint: str, params: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        return self._make_request("GET", endpoint, params=params)

    def post(
        self, endpoint: str, data: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        return self._make_request("POST", endpoint, data=data)

    def put(
        self, endpoint: str, data: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        return self._make_request("PUT", endpoint, data=data)

    def delete(self, endpoint: str) -> Dict[str, Any]:
        return self._make_request("DELETE", endpoint)

    def get_categories(self) -> Dict[str, Any]:
        return self.get("/categories")
