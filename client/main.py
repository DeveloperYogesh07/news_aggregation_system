import sys
import logging
from typing import Optional, Dict, Any
from ui.login_menu import LoginMenu
from ui.admin_menu import AdminMenu
from ui.user_menu import UserMenu
from services.api_client import APIClient
from utils.logger import setup_logger


def main() -> None:
    try:
        setup_logger()
        logger = logging.getLogger(__name__)
        logger.debug("Starting News Aggregation System Client")

        api_client = APIClient()

        while True:
            try:
                user = _handle_authentication(api_client)
                if user:
                    _handle_user_session(api_client, user)
            except KeyboardInterrupt:
                logger.info("Application terminated by user")
                print("\nGoodbye!")
                break
            except Exception as e:
                logger.error(f"Unexpected error in application: {e}")
                print(f"An unexpected error occurred: {e}")
                break

    except Exception as e:
        print(f"Failed to start application: {e}")
        sys.exit(1)


def _handle_authentication(api_client: APIClient) -> Optional[Dict[str, Any]]:
    try:
        login_menu = LoginMenu(api_client)
        return login_menu.show()
    except Exception as e:
        logger = logging.getLogger(__name__)
        logger.error(f"Authentication error: {e}")
        print("Authentication failed. Please try again.")
        return None


def _handle_user_session(api_client: APIClient, user: Dict[str, Any]) -> None:
    try:
        if user.get("is_admin"):
            logger = logging.getLogger(__name__)
            logger.info(f"Admin session started for user: {user.get('username')}")
            AdminMenu(api_client).show()
        else:
            logger = logging.getLogger(__name__)
            logger.info(f"User session started for user: {user.get('username')}")
            UserMenu(api_client).show()
    except Exception as e:
        logger = logging.getLogger(__name__)
        logger.error(f"Session error for user {user.get('username')}: {e}")
        print("Session error occurred. Please log in again.")


if __name__ == "__main__":
    main()
