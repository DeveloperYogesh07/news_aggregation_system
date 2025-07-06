
from typing import Optional


class UIConstants:
    # Header formatting
    HEADER_WIDTH = 50
    HEADER_CHAR = "="
    SEPARATOR_CHAR = "-"
    SEPARATOR_LENGTH = 40

    # Menu formatting
    MENU_INDENT = "    "
    MENU_OPTION_FORMAT = "[{number}] {description}"

    # Display formatting
    MAX_TITLE_LENGTH = 80
    MAX_CONTENT_PREVIEW = 200
    ITEMS_PER_PAGE = 10

    # Status indicators
    STATUS_ACTIVE = "Active"
    STATUS_INACTIVE = "Inactive"
    STATUS_ENABLED = "Enabled"
    STATUS_DISABLED = "Disabled"

    # Date/time formatting
    DATE_FORMAT = "%Y-%m-%d"
    TIME_FORMAT = "%I:%M %p"
    DATETIME_FORMAT = "%Y-%m-%d %H:%M"

    # Error and success messages
    ERROR_PREFIX = "❌ Error:"
    SUCCESS_PREFIX = "✅"
    INFO_PREFIX = "ℹ️"
    WARNING_PREFIX = "⚠️"

    # Default messages
    DEFAULT_PAUSE_MESSAGE = "Press Enter to continue..."
    DEFAULT_CONFIRMATION_MESSAGE = "Are you sure? (y/n): "
    DEFAULT_INPUT_PROMPT = "Enter your choice: "

    # Navigation
    BACK_OPTION = "Back"
    EXIT_OPTION = "Exit"
    LOGOUT_OPTION = "Logout"
    CANCEL_OPTION = "Cancel"

    # Article display
    ARTICLE_ID_PREFIX = "ID:"
    ARTICLE_TITLE_PREFIX = "Title:"
    ARTICLE_CONTENT_PREFIX = "Content:"
    ARTICLE_URL_PREFIX = "URL:"
    ARTICLE_SEPARATOR = "-" * 40

    # Server status display
    SERVER_NAME_PREFIX = "-"
    SERVER_STATUS_SEPARATOR = "|"
    SERVER_LAST_ACCESSED_PREFIX = "Last accessed:"

    # Notification display
    NOTIFICATION_PREFIX = "-"
    NOTIFICATION_DATE_FORMAT = "[{date}]"

    @classmethod
    def format_header(cls, title: str) -> str:
        header_line = cls.HEADER_CHAR * cls.HEADER_WIDTH
        centered_title = title.center(cls.HEADER_WIDTH)
        return f"\n{header_line}\n{centered_title}\n{header_line}"

    @classmethod
    def format_menu_option(cls, number: str, description: str) -> str:
        return cls.MENU_OPTION_FORMAT.format(number=number, description=description)

    @classmethod
    def format_separator(cls, length: Optional[int] = None) -> str:
        if length is None:
            length = cls.SEPARATOR_LENGTH
        return cls.SEPARATOR_CHAR * length

    @classmethod
    def truncate_text(cls, text: str, max_length: int) -> str:
        if len(text) <= max_length:
            return text
        return text[: max_length - 3] + "..."

    @classmethod
    def format_error_message(cls, message: str) -> str:
        return f"\n{cls.ERROR_PREFIX} {message}"

    @classmethod
    def format_success_message(cls, message: str) -> str:
        return f"\n{cls.SUCCESS_PREFIX} {message}"

    @classmethod
    def format_info_message(cls, message: str) -> str:
        return f"\n{cls.INFO_PREFIX} {message}"
