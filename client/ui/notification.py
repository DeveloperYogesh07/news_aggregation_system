import logging
from typing import Optional, Dict, Any, List
from datetime import datetime
from ui.base_menu import BaseMenu
from services.api_client import APIClient
from exceptions.custom_exceptions import (
    AuthenticationError,
    NetworkError,
    DataProcessingError,
)


class NotificationService:

    def __init__(self, api_client: APIClient):
        self.api_client = api_client
        self.logger = logging.getLogger(__name__)

    def get_notification_history(self) -> List[Dict[str, Any]]:
        try:
            response = self.api_client.get("/notifications/history")
            return response.get("data", []) if isinstance(response, dict) else response

        except Exception as e:
            self.logger.error(f"Failed to fetch notification history: {e}")
            raise DataProcessingError(
                "fetch notification history",
                f"Failed to fetch notification history: {e}",
            )

    def get_notification_configs(self) -> List[Dict[str, Any]]:
        try:
            response = self.api_client.get("/notifications/")
            return response.get("data", []) if isinstance(response, dict) else response

        except Exception as e:
            self.logger.error(f"Failed to fetch notification configs: {e}")
            raise DataProcessingError(
                "fetch notification configs",
                f"Failed to fetch notification configurations: {e}",
            )

    def toggle_category_notification(self, config_id: int, enabled: bool) -> None:
        try:
            self.api_client.put(f"/notifications/{config_id}", {"enabled": enabled})

        except Exception as e:
            self.logger.error(f"Failed to toggle notification {config_id}: {e}")
            raise DataProcessingError(
                "toggle notification", f"Failed to update notification setting: {e}"
            )

    def update_keywords(self, keywords: List[str]) -> None:
        try:
            self.api_client.put("/notifications/keywords", {"keywords": keywords})

        except Exception as e:
            self.logger.error(f"Failed to update keywords: {e}")
            raise DataProcessingError(
                "update keywords", f"Failed to update keywords: {e}"
            )


class NotificationMenu(BaseMenu):
    pass

    def __init__(self, api_client: APIClient):
        super().__init__()
        self.notification_service = NotificationService(api_client)

    def show(self) -> None:
        while True:
            try:
                self.print_header("N O T I F I C A T I O N S")
                self._display_welcome_message()
                choice = self._get_menu_choice()

                if choice == "1":
                    self._handle_view_notifications()
                elif choice == "2":
                    self._handle_configure_notifications()
                elif choice == "3":
                    return
                elif choice == "4":
                    self.display_info("Logging out...")
                    return
                else:
                    self.display_error("Invalid choice.")

            except KeyboardInterrupt:
                print("\nGoodbye!")
                return
            except Exception as e:
                self.logger.error(f"Unexpected error in notification menu: {e}")
                self.display_error("An unexpected error occurred. Please try again.")

    def _display_welcome_message(self) -> None:
        current_time = datetime.now()
        print(f"Welcome to News Application! Date: {current_time.strftime('%d-%b-%Y')}")
        print(f"Time: {current_time.strftime('%I:%M %p')}")

    def _get_menu_choice(self) -> str:
        print("\n1. View Notifications")
        print("2. Configure Notifications")
        print("3. Back")
        print("4. Logout")
        return input("Choice: ").strip()

    def _handle_view_notifications(self) -> None:
        try:
            notices = self.notification_service.get_notification_history()

            if not notices:
                self.display_info("No notifications yet.")
                self.pause()
                return

            print("\nNotifications:")
            for notice in notices:
                created_at = notice.get("created_at", "Unknown")
                message = notice.get("message", "No message")
                print(f"- [{created_at}] {message}")

            self.pause()

        except DataProcessingError as e:
            self.display_error(str(e))
            self.pause()
        except Exception as e:
            self.logger.error(f"Error viewing notifications: {e}")
            self.display_error("Failed to fetch notifications")
            self.pause()

    def _handle_configure_notifications(self) -> None:
        try:
            configs = self.notification_service.get_notification_configs()

            if not configs:
                self.display_info("No notification configurations found.")
                return

            self._show_configuration_menu(configs)

        except DataProcessingError as e:
            self.display_error(str(e))
            self.pause()
        except Exception as e:
            self.logger.error(f"Error configuring notifications: {e}")
            self.display_error("Failed to load notification configurations")
            self.pause()

    def _show_configuration_menu(self, configs: List[Dict[str, Any]]) -> None:
        while True:
            try:
                self.print_header("C O N F I G U R E - N O T I F I C A T I O N S")
                mapping = {}

                for idx, config in enumerate(configs, 1):
                    label = config.get("category") or "Keywords"
                    status = "Enabled" if config.get("enabled") else "Disabled"
                    print(f"{idx}. {label} - {status}")
                    mapping[str(idx)] = config

                back_option = str(len(configs) + 1)
                logout_option = str(len(configs) + 2)

                print(f"{back_option}. Back")
                print(f"{logout_option}. Logout")

                option = self.get_user_input("Enter your option: ")
                if not option:
                    continue

                if option == back_option:
                    return
                elif option == logout_option:
                    self.display_info("Logging out...")
                    return
                elif option in mapping:
                    selected = mapping[option]
                    self._handle_configuration_toggle(selected)
                else:
                    self.display_error("Invalid option.")

            except KeyboardInterrupt:
                return
            except Exception as e:
                self.logger.error(f"Error in configuration menu: {e}")
                self.display_error("An error occurred. Please try again.")

    def _handle_configuration_toggle(self, config: Dict[str, Any]) -> None:
        try:
            if config.get("category"):
                new_value = not config.get("enabled", False)
                self.notification_service.toggle_category_notification(
                    config["id"], new_value
                )

                status = "enabled" if new_value else "disabled"
                self.display_success(f"{config['category']} notification {status}.")

            else:
                self._handle_keyword_update()

        except DataProcessingError as e:
            self.display_error(str(e))
        except Exception as e:
            self.logger.error(f"Error toggling configuration: {e}")
            self.display_error("Update failed")

        self.pause()

    def _handle_keyword_update(self) -> None:
        try:
            keywords_input = self.get_user_input("Enter comma-separated keywords: ")
            if not keywords_input:
                self.display_error("Keyword list cannot be empty.")
                return

            keywords = [k.strip() for k in keywords_input.split(",") if k.strip()]

            if not keywords:
                self.display_error("No valid keywords provided.")
                return

            self.notification_service.update_keywords(keywords)
            self.display_success("Keywords updated successfully.")

        except DataProcessingError as e:
            self.display_error(str(e))
        except Exception as e:
            self.logger.error(f"Error updating keywords: {e}")
            self.display_error("Failed to update keywords")
