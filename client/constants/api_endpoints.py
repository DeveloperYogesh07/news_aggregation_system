

class APIEndpoints:

    # Authentication endpoints
    LOGIN = "/auth/login"
    SIGNUP = "/auth/signup"

    # User endpoints
    USER_PROFILE = "/users/me"

    # Article endpoints
    ARTICLES = "/articles/"
    ARTICLES_RANGE = "/articles/range"
    ARTICLES_SEARCH = "/articles/search"
    ARTICLE_REPORT = "/articles/report/{article_id}"
    ARTICLE_HIDE = "/admin/articles/{article_id}/hide"

    # Category endpoints
    CATEGORIES = "/categories/"
    CATEGORY_HIDE = "/admin/categories/{category_id}/hide"
    CATEGORY_CREATE = "/admin/categories/"

    # Saved articles endpoints
    SAVED_ARTICLES = "/saved-articles/"

    # Vote endpoints
    VOTES = "/votes/"

    # Notification endpoints
    NOTIFICATIONS = "/notifications/"
    NOTIFICATION_HISTORY = "/notifications/history"
    NOTIFICATION_KEYWORDS = "/notifications/keywords"
    NOTIFICATION_UPDATE = "/notifications/{notification_id}"

    # Admin endpoints
    EXTERNAL_SOURCES = "/admin/external-sources"
    EXTERNAL_SOURCE_UPDATE = "/admin/external-sources/{server_id}"
    REPORTED_ARTICLES = "/admin/reported-articles"
    BLACKLIST_KEYWORD = "/admin/blacklist-keyword"

    @classmethod
    def format_article_report(cls, article_id: str) -> str:
        """Format article report endpoint with article ID."""
        return cls.ARTICLE_REPORT.format(article_id=article_id)

    @classmethod
    def format_article_hide(cls, article_id: str) -> str:
        """Format article hide endpoint with article ID."""
        return cls.ARTICLE_HIDE.format(article_id=article_id)

    @classmethod
    def format_category_hide(cls, category_id: str) -> str:
        """Format category hide endpoint with category ID."""
        return cls.CATEGORY_HIDE.format(category_id=category_id)

    @classmethod
    def format_external_source_update(cls, server_id: str) -> str:
        """Format external source update endpoint with server ID."""
        return cls.EXTERNAL_SOURCE_UPDATE.format(server_id=server_id)

    @classmethod
    def format_notification_update(cls, notification_id: str) -> str:
        """Format notification update endpoint with notification ID."""
        return cls.NOTIFICATION_UPDATE.format(notification_id=notification_id)
