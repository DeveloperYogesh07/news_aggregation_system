from sqlalchemy.orm import Session
from app.core.security import verify_password, get_password_hash, create_access_token
from app.repositories.user_repository import UserRepository
from app.schemas.auth import Token
from app.schemas.user import UserCreate
from app.exceptions.custom_exceptions import (
    AuthenticationException,
    ValidationException,
    UserException,
)


class AuthService:

    def __init__(self, db: Session):
        self.db = db

    def authenticate_user(self, email: str, password: str) -> Token:
        try:
            if not email or not password:
                raise ValidationException(
                    "Email and password are required", field="credentials"
                )

            user = UserRepository.get_by_email(self.db, email)
            if not user or not verify_password(password, user.hashed_password):  # type: ignore
                raise AuthenticationException("Invalid email or password")

            token = create_access_token({"user_id": user.id})
            return Token(access_token=token)
        except (AuthenticationException, ValidationException):
            raise
        except Exception as e:
            raise AuthenticationException(f"Authentication failed: {str(e)}")

    def register_user(self, user_create: UserCreate) -> Token:
        try:
            if (
                not user_create.email
                or not user_create.password
                or not user_create.username
            ):
                raise ValidationException(
                    "Username, email, and password are required", field="user_data"
                )

            existing_user = UserRepository.get_by_email(self.db, user_create.email)
            if existing_user:
                raise UserException(
                    "User with this email already exists", operation="register"
                )

            hashed_pw = get_password_hash(user_create.password)
            new_user = UserRepository.create(
                self.db, user_create.username, user_create.email, hashed_pw
            )
            token = create_access_token({"user_id": new_user.id})
            return Token(access_token=token)
        except (ValidationException, UserException):
            raise
        except Exception as e:
            raise UserException(
                f"User registration failed: {str(e)}", operation="register"
            )
