"""
Custom exceptions for the News Aggregation System Client.
"""

from .custom_exceptions import (
    ClientError,
    ValidationError,
    ConfigurationError,
    UserInputError,
    DisplayError,
)

__all__ = [
    "ClientError",
    "ValidationError",
    "ConfigurationError",
    "UserInputError",
    "DisplayError",
]
