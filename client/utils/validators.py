import re


def validate_email(email: str) -> bool:
    if not email or not isinstance(email, str):
        return False

    pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    return bool(re.match(pattern, email.strip()))


def validate_password(password: str) -> bool:
    if not password or not isinstance(password, str):
        return False

    return len(password.strip()) >= 3


def validate_username(username: str) -> bool:
    if not username or not isinstance(username, str):
        return False

    username = username.strip()

    if len(username) < 3 or len(username) > 20:
        return False

    pattern = r"^[a-zA-Z0-9_]+$"
    return bool(re.match(pattern, username))
