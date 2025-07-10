from pydantic_settings import BaseSettings
from typing import ClassVar


class Settings(BaseSettings):
    API_V1_STR: str = "/api/v1"
    SECRET_KEY: str = "" 
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    SQLALCHEMY_DATABASE_URI: ClassVar[str] = "sqlite:///./database.db"

    SMTP_SERVER: str = "smtp.gmail.com"
    SMTP_PORT: int = 587
    SMTP_USER: str = "yogiupadhyay07@gmail.com"
    SMTP_PASSWORD: str = ""  

    class Config:
        env_file = ".env"


settings = Settings()

if not settings.SECRET_KEY:
    raise ValueError("SECRET_KEY environment variable must be set")
if not settings.SMTP_PASSWORD:
    raise ValueError("SMTP_PASSWORD environment variable must be set")
