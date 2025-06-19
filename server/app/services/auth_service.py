from sqlalchemy.orm import Session
from app.core.security import verify_password, get_password_hash, create_access_token
from app.repositories.user_repository import UserRepository
from app.schemas.auth import Token
from app.schemas.user import UserCreate

class AuthService:

    def __init__(self, db: Session):
        self.db = db

    def authenticate_user(self, email: str, password: str) -> Token:
        user = UserRepository.get_by_email(self.db, email)
        if not user or not verify_password(password, user.hashed_password):
            raise ValueError("Invalid credentials")
        token = create_access_token({"user_id": user.id})
        return Token(access_token=token)

    def register_user(self, user_create: UserCreate) -> Token:
        existing_user = UserRepository.get_by_email(self.db, user_create.email)
        if existing_user:
            raise ValueError("User already exists")
        hashed_pw = get_password_hash(user_create.password)
        new_user = UserRepository.create(self.db, user_create.username, user_create.email, hashed_pw)
        token = create_access_token({"user_id": new_user.id})
        return Token(access_token=token)

