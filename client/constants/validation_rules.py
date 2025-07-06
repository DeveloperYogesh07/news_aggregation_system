import re


class ValidationRules:

    # Length constraints
    MIN_USERNAME_LENGTH = 3
    MAX_USERNAME_LENGTH = 20
    MIN_PASSWORD_LENGTH = 3
    MAX_PASSWORD_LENGTH = 128
    MIN_EMAIL_LENGTH = 5
    MAX_EMAIL_LENGTH = 254

    # Patterns
    USERNAME_PATTERN = r"^[a-zA-Z0-9_]+$"
    EMAIL_PATTERN = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    DATE_PATTERN = r"^\d{4}-\d{2}-\d{2}$"

    # Compiled patterns for performance
    USERNAME_REGEX = re.compile(USERNAME_PATTERN)
    EMAIL_REGEX = re.compile(EMAIL_PATTERN)
    DATE_REGEX = re.compile(DATE_PATTERN)

    # Error messages
    USERNAME_TOO_SHORT = (
        f"Username must be at least {MIN_USERNAME_LENGTH} characters long"
    )
    USERNAME_TOO_LONG = (
        f"Username must be no more than {MAX_USERNAME_LENGTH} characters long"
    )
    USERNAME_INVALID_CHARS = (
        "Username can only contain letters, numbers, and underscores"
    )
    PASSWORD_TOO_SHORT = (
        f"Password must be at least {MIN_PASSWORD_LENGTH} characters long"
    )
    PASSWORD_TOO_LONG = (
        f"Password must be no more than {MAX_PASSWORD_LENGTH} characters long"
    )
    EMAIL_INVALID_FORMAT = "Please enter a valid email address"
    EMAIL_TOO_SHORT = f"Email must be at least {MIN_EMAIL_LENGTH} characters long"
    EMAIL_TOO_LONG = f"Email must be no more than {MAX_EMAIL_LENGTH} characters long"
    DATE_INVALID_FORMAT = "Date must be in YYYY-MM-DD format"
    REQUIRED_FIELD = "This field is required"

    @classmethod
    def validate_username(cls, username: str) -> tuple[bool, str]:
        if not username:
            return False, cls.REQUIRED_FIELD

        username = username.strip()

        if len(username) < cls.MIN_USERNAME_LENGTH:
            return False, cls.USERNAME_TOO_SHORT

        if len(username) > cls.MAX_USERNAME_LENGTH:
            return False, cls.USERNAME_TOO_LONG

        if not cls.USERNAME_REGEX.match(username):
            return False, cls.USERNAME_INVALID_CHARS

        return True, ""

    @classmethod
    def validate_password(cls, password: str) -> tuple[bool, str]:
        if not password:
            return False, cls.REQUIRED_FIELD

        password = password.strip()

        if len(password) < cls.MIN_PASSWORD_LENGTH:
            return False, cls.PASSWORD_TOO_SHORT

        if len(password) > cls.MAX_PASSWORD_LENGTH:
            return False, cls.PASSWORD_TOO_LONG

        return True, ""

    @classmethod
    def validate_email(cls, email: str) -> tuple[bool, str]:
        if not email:
            return False, cls.REQUIRED_FIELD

        email = email.strip()

        if len(email) < cls.MIN_EMAIL_LENGTH:
            return False, cls.EMAIL_TOO_SHORT

        if len(email) > cls.MAX_EMAIL_LENGTH:
            return False, cls.EMAIL_TOO_LONG

        if not cls.EMAIL_REGEX.match(email):
            return False, cls.EMAIL_INVALID_FORMAT

        return True, ""

    @classmethod
    def validate_date(cls, date_str: str) -> tuple[bool, str]:
        if not date_str:
            return False, cls.REQUIRED_FIELD

        if not cls.DATE_REGEX.match(date_str):
            return False, cls.DATE_INVALID_FORMAT

        return True, ""
