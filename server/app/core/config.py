from pydantic_settings import BaseSettings
from typing import ClassVar


class Settings(BaseSettings):
    API_V1_STR: str = "/api/v1"
    SECRET_KEY: str = "supersecretkey"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    SQLALCHEMY_DATABASE_URI: ClassVar[str] = "sqlite:///./test.db"

    SMTP_SERVER: str = "smtp.gmail.com"
    SMTP_PORT: int = 587
    SMTP_USER: str = "yogiupadhyay07@gmail.com"
    SMTP_PASSWORD: str = "pxxr cpfk pwye ozci"

    class Config:
        env_file = ".env"


settings = Settings()
