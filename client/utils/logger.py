import logging
import sys
import os
from typing import Optional


def setup_logger(
    level: int = None,
    log_format: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    log_file: Optional[str] = None,
) -> None:
    # Allow environment variable override
    if level is None:
        level = getattr(logging, os.getenv("LOG_LEVEL", "WARNING").upper(), logging.WARNING)
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)  # Capture all levels

    logger.handlers.clear()

    # Console handler - only show WARNING and above for clean UI
    console_formatter = logging.Formatter("%(levelname)s: %(message)s")
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.WARNING)
    console_handler.setFormatter(console_formatter)
    logger.addHandler(console_handler)

    # File handler - log everything for debugging
    if log_file:
        try:
            file_formatter = logging.Formatter(log_format)
            file_handler = logging.FileHandler(log_file)
            file_handler.setLevel(logging.DEBUG)
            file_handler.setFormatter(file_formatter)
            logger.addHandler(file_handler)
        except Exception as e:
            print(f"Warning: Could not setup file logging to {log_file}: {e}")
    else:
        # If no file specified, create a default debug log
        try:
            file_formatter = logging.Formatter(log_format)
            file_handler = logging.FileHandler("debug.log")
            file_handler.setLevel(logging.DEBUG)
            file_handler.setFormatter(file_formatter)
            logger.addHandler(file_handler)
        except Exception:
            pass  # Silently fail if we can't create debug log


def get_logger(name: str) -> logging.Logger:
    return logging.getLogger(name)
