import re


class ValidationRules:

    MIN_USERNAME_LENGTH = 3
    MAX_USERNAME_LENGTH = 20
    MIN_PASSWORD_LENGTH = 3
    MAX_PASSWORD_LENGTH = 128

    USERNAME_PATTERN = r"^[a-zA-Z0-9_]+$"
    EMAIL_PATTERN = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"

    USERNAME_REGEX = re.compile(USERNAME_PATTERN)
    EMAIL_REGEX = re.compile(EMAIL_PATTERN)

    @classmethod
    def validate_username(cls, username: str) -> tuple[bool, str]:
        """Validate username format and length."""
        if not username:
            return False, "Username is required"

        username = username.strip()

        if len(username) < cls.MIN_USERNAME_LENGTH:
            return (
                False,
                f"Username must be at least {cls.MIN_USERNAME_LENGTH} characters",
            )

        if len(username) > cls.MAX_USERNAME_LENGTH:
            return (
                False,
                f"Username must be no more than {cls.MAX_USERNAME_LENGTH} characters",
            )

        if not cls.USERNAME_REGEX.match(username):
            return False, "Username can only contain letters, numbers, and underscores"

        return True, ""

    @classmethod
    def validate_password(cls, password: str) -> tuple[bool, str]:
        """Validate password length."""
        if not password:
            return False, "Password is required"

        password = password.strip()

        if len(password) < cls.MIN_PASSWORD_LENGTH:
            return (
                False,
                f"Password must be at least {cls.MIN_PASSWORD_LENGTH} characters",
            )

        if len(password) > cls.MAX_PASSWORD_LENGTH:
            return (
                False,
                f"Password must be no more than {cls.MAX_PASSWORD_LENGTH} characters",
            )

        return True, ""

    @classmethod
    def validate_email(cls, email: str) -> tuple[bool, str]:
        """Validate email format."""
        if not email:
            return False, "Email is required"

        email = email.strip()

        if not cls.EMAIL_REGEX.match(email):
            return False, "Please enter a valid email address"

        return True, ""
