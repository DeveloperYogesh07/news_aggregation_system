from typing import Optional


class NewsAggregatorException(Exception):
    """Base exception for all News Aggregator exceptions."""

    def __init__(
        self,
        message: str,
        error_code: Optional[str] = None,
        details: Optional[dict] = None,
    ):
        self.message = message
        self.error_code = error_code
        self.details = details or {}
        super().__init__(self.message)


class DatabaseException(NewsAggregatorException):
    """Raised when database operations fail."""

    def __init__(
        self, message: str, operation: Optional[str] = None, table: Optional[str] = None
    ):
        super().__init__(message, "DB_ERROR", {"operation": operation, "table": table})


class ValidationException(NewsAggregatorException):
    """Raised when data validation fails."""

    def __init__(
        self, message: str, field: Optional[str] = None, value: Optional[str] = None
    ):
        super().__init__(message, "VALIDATION_ERROR", {"field": field, "value": value})


class AuthenticationException(NewsAggregatorException):
    """Raised when authentication fails."""

    def __init__(self, message: str, user_id: Optional[int] = None):
        super().__init__(message, "AUTH_ERROR", {"user_id": user_id})


class AuthorizationException(NewsAggregatorException):
    """Raised when authorization fails."""

    def __init__(
        self,
        message: str,
        user_id: Optional[int] = None,
        required_role: Optional[str] = None,
    ):
        super().__init__(
            message,
            "AUTHORIZATION_ERROR",
            {"user_id": user_id, "required_role": required_role},
        )


class ExternalAPIException(NewsAggregatorException):
    """Raised when external API calls fail."""

    def __init__(
        self,
        message: str,
        api_name: Optional[str] = None,
        status_code: Optional[int] = None,
    ):
        super().__init__(
            message,
            "EXTERNAL_API_ERROR",
            {"api_name": api_name, "status_code": status_code},
        )


class NotificationException(NewsAggregatorException):
    """Raised when notification operations fail."""

    def __init__(
        self,
        message: str,
        notification_type: Optional[str] = None,
        user_id: Optional[int] = None,
    ):
        super().__init__(
            message,
            "NOTIFICATION_ERROR",
            {"notification_type": notification_type, "user_id": user_id},
        )


class EmailException(NewsAggregatorException):
    """Raised when email operations fail."""

    def __init__(
        self,
        message: str,
        recipient: Optional[str] = None,
        subject: Optional[str] = None,
    ):
        super().__init__(
            message, "EMAIL_ERROR", {"recipient": recipient, "subject": subject}
        )


class ArticleException(NewsAggregatorException):
    """Raised when article operations fail."""

    def __init__(
        self,
        message: str,
        article_id: Optional[int] = None,
        operation: Optional[str] = None,
    ):
        super().__init__(
            message, "ARTICLE_ERROR", {"article_id": article_id, "operation": operation}
        )


class CategoryException(NewsAggregatorException):
    """Raised when category operations fail."""

    def __init__(
        self,
        message: str,
        category_name: Optional[str] = None,
        operation: Optional[str] = None,
    ):
        super().__init__(
            message,
            "CATEGORY_ERROR",
            {"category_name": category_name, "operation": operation},
        )


class UserException(NewsAggregatorException):
    """Raised when user operations fail."""

    def __init__(
        self,
        message: str,
        user_id: Optional[int] = None,
        operation: Optional[str] = None,
    ):
        super().__init__(
            message, "USER_ERROR", {"user_id": user_id, "operation": operation}
        )


class ConfigurationException(NewsAggregatorException):
    """Raised when configuration is invalid."""

    def __init__(self, message: str, config_key: Optional[str] = None):
        super().__init__(message, "CONFIG_ERROR", {"config_key": config_key})


class SchedulerException(NewsAggregatorException):
    """Raised when scheduler operations fail."""

    def __init__(self, message: str, job_name: Optional[str] = None):
        super().__init__(message, "SCHEDULER_ERROR", {"job_name": job_name})
