
from typing import Optional, Any, Dict


class ClientError(Exception):

    def __init__(self, message: str, details: Optional[Dict[str, Any]] = None):
        super().__init__(message)
        self.message = message
        self.details = details or {}

    def __str__(self) -> str:
        """Return string representation of the error."""
        return self.message


class ValidationError(ClientError):

    def __init__(self, field: str, message: str, value: Optional[Any] = None):
        super().__init__(f"Validation error for {field}: {message}")
        self.field = field
        self.value = value


class ConfigurationError(ClientError):

    def __init__(self, config_key: str, message: str):
        super().__init__(f"Configuration error for {config_key}: {message}")
        self.config_key = config_key


class UserInputError(ClientError):
    def __init__(self, input_type: str, message: str, user_input: Optional[str] = None):
        super().__init__(f"Input error for {input_type}: {message}")
        self.input_type = input_type
        self.user_input = user_input


class DisplayError(ClientError):
    def __init__(self, component: str, message: str):
        super().__init__(f"Display error in {component}: {message}")
        self.component = component


class AuthenticationError(ClientError):
    def __init__(self, operation: str, message: str, status_code: Optional[int] = None):
        super().__init__(f"Authentication error during {operation}: {message}")
        self.operation = operation
        self.status_code = status_code


class NetworkError(ClientError):
    def __init__(self, operation: str, message: str, url: Optional[str] = None):
        super().__init__(f"Network error during {operation}: {message}")
        self.operation = operation
        self.url = url


class DataProcessingError(ClientError):
    def __init__(self, operation: str, message: str, data_type: Optional[str] = None):
        super().__init__(f"Data processing error during {operation}: {message}")
        self.operation = operation
        self.data_type = data_type


class TimeoutError(ClientError):

    def __init__(self, operation: str, timeout_seconds: int):
        super().__init__(
            f"Operation '{operation}' timed out after {timeout_seconds} seconds"
        )
        self.operation = operation
        self.timeout_seconds = timeout_seconds
