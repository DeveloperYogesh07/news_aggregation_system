from typing import Optional

class NewsAggregatorException(Exception):
    """Base exception for all News Aggregator exceptions."""
    
    def __init__(self, message: str, error_code: str = None, details: dict = None):
        self.message = message
        self.error_code = error_code
        self.details = details or {}
        super().__init__(self.message)


class DatabaseException(NewsAggregatorException):
    """Raised when database operations fail."""
    
    def __init__(self, message: str, operation: str = None, table: str = None):
        super().__init__(message, "DB_ERROR", {"operation": operation, "table": table})


class ValidationException(NewsAggregatorException):
    """Raised when data validation fails."""
    
    def __init__(self, message: str, field: str = None, value: str = None):
        super().__init__(message, "VALIDATION_ERROR", {"field": field, "value": value})


class AuthenticationException(NewsAggregatorException):
    """Raised when authentication fails."""
    
    def __init__(self, message: str, user_id: int = None):
        super().__init__(message, "AUTH_ERROR", {"user_id": user_id})


class AuthorizationException(NewsAggregatorException):
    """Raised when authorization fails."""
    
    def __init__(self, message: str, user_id: int = None, required_role: str = None):
        super().__init__(message, "AUTHORIZATION_ERROR", {"user_id": user_id, "required_role": required_role})


class ExternalAPIException(NewsAggregatorException):
    """Raised when external API calls fail."""
    
    def __init__(self, message: str, api_name: str = None, status_code: int = None):
        super().__init__(message, "EXTERNAL_API_ERROR", {"api_name": api_name, "status_code": status_code})


class NotificationException(NewsAggregatorException):
    """Raised when notification operations fail."""
    
    def __init__(self, message: str, notification_type: str = None, user_id: int = None):
        super().__init__(message, "NOTIFICATION_ERROR", {"notification_type": notification_type, "user_id": user_id})


class EmailException(NewsAggregatorException):
    """Raised when email operations fail."""
    
    def __init__(self, message: str, recipient: Optional[str] = None, subject: str = None):
        super().__init__(message, "EMAIL_ERROR", {"recipient": recipient, "subject": subject})


class ArticleException(NewsAggregatorException):
    """Raised when article operations fail."""
    
    def __init__(self, message: str, article_id: int = None, operation: str = None):
        super().__init__(message, "ARTICLE_ERROR", {"article_id": article_id, "operation": operation})


class CategoryException(NewsAggregatorException):
    """Raised when category operations fail."""
    
    def __init__(self, message: str, category_name: str = None, operation: str = None):
        super().__init__(message, "CATEGORY_ERROR", {"category_name": category_name, "operation": operation})


class UserException(NewsAggregatorException):
    """Raised when user operations fail."""
    
    def __init__(self, message: str, user_id: int = None, operation: str = None):
        super().__init__(message, "USER_ERROR", {"user_id": user_id, "operation": operation})


class ConfigurationException(NewsAggregatorException):
    """Raised when configuration is invalid."""
    
    def __init__(self, message: str, config_key: str = None):
        super().__init__(message, "CONFIG_ERROR", {"config_key": config_key})


class SchedulerException(NewsAggregatorException):
    """Raised when scheduler operations fail."""
    
    def __init__(self, message: str, job_name: str = None):
        super().__init__(message, "SCHEDULER_ERROR", {"job_name": job_name}) 