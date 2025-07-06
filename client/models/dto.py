from dataclasses import dataclass, field
from typing import Optional, List, Dict, Any
from datetime import datetime


@dataclass
class UserDTO:
    id: int
    username: str
    email: str
    is_admin: bool
    created_at: Optional[str] = None
    updated_at: Optional[str] = None

    def __post_init__(self):
        """Validate user data after initialization."""
        if not self.username or not self.email:
            raise ValueError("Username and email are required")
        if not isinstance(self.is_admin, bool):
            raise ValueError("is_admin must be a boolean")


@dataclass
class ArticleDTO:
    id: int
    title: str
    content: Optional[str] = None
    url: Optional[str] = None
    category: Optional[str] = None
    published_at: Optional[str] = None
    created_at: Optional[str] = None
    updated_at: Optional[str] = None
    source: Optional[str] = None

    def __post_init__(self):
        """Validate article data after initialization."""
        if not self.title:
            raise ValueError("Article title is required")


@dataclass
class SavedArticleDTO:
    id: int
    article_id: int
    title: str
    content: Optional[str] = None
    url: Optional[str] = None
    saved_at: Optional[str] = None
    user_id: Optional[int] = None

    def __post_init__(self):
        """Validate saved article data after initialization."""
        if not self.title:
            raise ValueError("Article title is required")


@dataclass
class CategoryDTO:
    id: int
    name: str
    is_active: bool = True
    created_at: Optional[str] = None
    updated_at: Optional[str] = None

    def __post_init__(self):
        """Validate category data after initialization."""
        if not self.name:
            raise ValueError("Category name is required")


@dataclass
class NotificationDTO:
    id: int
    message: str
    category: Optional[str] = None
    is_read: bool = False
    created_at: Optional[str] = None
    user_id: Optional[int] = None

    def __post_init__(self):
        """Validate notification data after initialization."""
        if not self.message:
            raise ValueError("Notification message is required")


@dataclass
class NotificationConfigDTO:
    id: int
    category: Optional[str] = None
    enabled: bool = True
    keywords: List[str] = field(default_factory=list)
    created_at: Optional[str] = None
    updated_at: Optional[str] = None


@dataclass
class ExternalSourceDTO:

    id: int
    name: str
    api_key: Optional[str] = None
    is_active: bool = True
    last_accessed: Optional[str] = None
    created_at: Optional[str] = None
    updated_at: Optional[str] = None

    def __post_init__(self):
        """Validate external source data after initialization."""
        if not self.name:
            raise ValueError("External source name is required")


@dataclass
class ArticleReportDTO:
    id: int
    article_id: int
    reason: Optional[str] = None
    reported_at: Optional[str] = None
    reporter_id: Optional[int] = None

    def __post_init__(self):
        """Validate article report data after initialization."""
        if self.article_id <= 0:
            raise ValueError("Article ID must be positive")


@dataclass
class VoteDTO:
    id: int
    article_id: int
    vote_type: str  # 'like' or 'dislike'
    user_id: Optional[int] = None
    created_at: Optional[str] = None

    def __post_init__(self):
        """Validate vote data after initialization."""
        if self.article_id <= 0:
            raise ValueError("Article ID must be positive")
        if self.vote_type not in ["like", "dislike"]:
            raise ValueError("Vote type must be 'like' or 'dislike'")


@dataclass
class LoginRequestDTO:
    email: str
    password: str

    def __post_init__(self):
        """Validate login request data after initialization."""
        if not self.email or not self.password:
            raise ValueError("Email and password are required")


@dataclass
class SignupRequestDTO:
    username: str
    email: str
    password: str

    def __post_init__(self):
        """Validate signup request data after initialization."""
        if not self.username or not self.email or not self.password:
            raise ValueError("Username, email, and password are required")


@dataclass
class ArticleSearchRequestDTO:
    query: str
    category: Optional[str] = None
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    limit: Optional[int] = None

    def __post_init__(self):
        """Validate search request data after initialization."""
        if not self.query:
            raise ValueError("Search query is required")


@dataclass
class APIResponseDTO:
    success: bool
    data: Optional[Any] = None
    message: Optional[str] = None
    error_code: Optional[str] = None
    timestamp: Optional[str] = None

    def __post_init__(self):
        """Validate API response data after initialization."""
        if not isinstance(self.success, bool):
            raise ValueError("Success must be a boolean")


@dataclass
class PaginationDTO:
    page: int
    per_page: int
    total: int
    total_pages: int
    has_next: bool
    has_prev: bool

    def __post_init__(self):
        """Validate pagination data after initialization."""
        if self.page <= 0 or self.per_page <= 0:
            raise ValueError("Page and per_page must be positive")
        if self.total < 0:
            raise ValueError("Total cannot be negative")


@dataclass
class ErrorDTO:
    code: str
    message: str
    details: Optional[Dict[str, Any]] = None
    timestamp: Optional[str] = None

    def __post_init__(self):
        """Validate error data after initialization."""
        if not self.code or not self.message:
            raise ValueError("Error code and message are required")
