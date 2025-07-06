import os
from typing import Optional
from dataclasses import dataclass


@dataclass
class Settings:
    API_BASE_URL: str = "http://127.0.0.1:8000/api/v1"
    API_TIMEOUT: int = 30
    API_RETRY_ATTEMPTS: int = 3

    LOG_LEVEL: str = "INFO"
    LOG_FORMAT: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    LOG_FILE: Optional[str] = None

    MENU_TIMEOUT: int = 300  # 5 minutes
    MAX_DISPLAY_ITEMS: int = 50

    DATE_FORMAT: str = "%Y-%m-%d"
    TIME_FORMAT: str = "%I:%M %p"
    DATETIME_FORMAT: str = "%Y-%m-%d %H:%M"

    def __post_init__(self):
        self._load_from_environment()

    def _load_from_environment(self) -> None:
        self.API_BASE_URL = os.getenv("API_BASE_URL", self.API_BASE_URL)
        self.API_TIMEOUT = int(os.getenv("API_TIMEOUT", str(self.API_TIMEOUT)))
        self.API_RETRY_ATTEMPTS = int(
            os.getenv("API_RETRY_ATTEMPTS", str(self.API_RETRY_ATTEMPTS))
        )

        self.LOG_LEVEL = os.getenv("LOG_LEVEL", self.LOG_LEVEL)
        self.LOG_FORMAT = os.getenv("LOG_FORMAT", self.LOG_FORMAT)
        self.LOG_FILE = os.getenv("LOG_FILE", self.LOG_FILE)

        self.MENU_TIMEOUT = int(os.getenv("MENU_TIMEOUT", str(self.MENU_TIMEOUT)))
        self.MAX_DISPLAY_ITEMS = int(
            os.getenv("MAX_DISPLAY_ITEMS", str(self.MAX_DISPLAY_ITEMS))
        )

    def validate(self) -> None:
        if not self.API_BASE_URL:
            raise ValueError("API_BASE_URL cannot be empty")

        if self.API_TIMEOUT <= 0:
            raise ValueError("API_TIMEOUT must be positive")

        if self.API_RETRY_ATTEMPTS < 0:
            raise ValueError("API_RETRY_ATTEMPTS cannot be negative")

    def get_api_url(self, endpoint: str) -> str:
        base_url = self.API_BASE_URL.rstrip("/")
        if not endpoint.startswith("/"):
            endpoint = "/" + endpoint
        return f"{base_url}{endpoint}"


settings = Settings()
