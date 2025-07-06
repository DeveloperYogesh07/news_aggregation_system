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


class AdminService:

    def __init__(self, api_client: APIClient):
        self.api_client = api_client
        self.logger = logging.getLogger(__name__)

    def get_external_servers(self) -> List[Dict[str, Any]]:
        try:
            response = self.api_client.get("/admin/external-sources")
            return response.get("data", []) if isinstance(response, dict) else response
        except Exception as e:
            self.logger.error(f"Failed to fetch external servers: {e}")
            raise DataProcessingError(
                "fetch external servers", f"Failed to fetch external servers: {e}"
            )

    def update_external_server(self, server_id: str, api_key: str) -> None:
        try:
            self.api_client.put(
                f"/admin/external-sources/{server_id}", {"api_key": api_key}
            )
        except Exception as e:
            self.logger.error(f"Failed to update external server {server_id}: {e}")
            raise DataProcessingError(
                "update external server", f"Failed to update external server: {e}"
            )

    def add_category(self, name: str) -> None:
        try:
            self.api_client.post("/admin/categories/", {"name": name})
        except Exception as e:
            self.logger.error(f"Failed to add category '{name}': {e}")
            raise DataProcessingError("add category", f"Failed to add category: {e}")

    def get_reported_articles(self) -> List[Dict[str, Any]]:
        try:
            response = self.api_client.get("/admin/reported-articles")
            return response.get("data", []) if isinstance(response, dict) else response
        except Exception as e:
            self.logger.error(f"Failed to fetch reported articles: {e}")
            raise DataProcessingError(
                "fetch reported articles", f"Failed to fetch reported articles: {e}"
            )

    def hide_article(self, article_id: str) -> None:
        try:
            self.api_client.put(f"/admin/articles/{article_id}/hide", {})
        except Exception as e:
            self.logger.error(f"Failed to hide article {article_id}: {e}")
            raise DataProcessingError("hide article", f"Failed to hide article: {e}")

    def hide_category(self, category_id: str) -> None:
        try:
            self.api_client.put(f"/admin/categories/{category_id}/hide", {})
        except Exception as e:
            self.logger.error(f"Failed to hide category {category_id}: {e}")
            raise DataProcessingError("hide category", f"Failed to hide category: {e}")

    def blacklist_keyword(self, keyword: str) -> None:
        try:
            self.api_client.post("/admin/blacklist-keyword", {"keyword": keyword})
        except Exception as e:
            self.logger.error(f"Failed to blacklist keyword '{keyword}': {e}")
            raise DataProcessingError(
                "blacklist keyword", f"Failed to blacklist keyword: {e}"
            )

    def get_categories(self) -> List[Dict[str, Any]]:
        try:
            response = self.api_client.get("/categories/")
            return response.get("data", []) if isinstance(response, dict) else response
        except Exception as e:
            self.logger.error(f"Failed to fetch categories: {e}")
            raise DataProcessingError(
                "fetch categories", f"Failed to fetch categories: {e}"
            )


class AdminMenu(BaseMenu):
    pass

    def __init__(self, api_client: APIClient):
        super().__init__()
        self.admin_service = AdminService(api_client)

    def show(self) -> None:
        while True:
            try:
                self.print_header("Admin Menu")
                choice = self._get_menu_choice()

                if choice == "1":
                    self._handle_view_servers()
                elif choice == "2":
                    self._handle_update_server()
                elif choice == "3":
                    self._handle_add_category()
                elif choice == "4":
                    self._handle_view_reports()
                elif choice == "5":
                    self._handle_hide_category()
                elif choice == "6":
                    self._handle_blacklist_keyword()
                elif choice == "7":
                    self.display_info("Logging out...")
                    return
                else:
                    self.display_error("Invalid choice. Please try again.")

            except KeyboardInterrupt:
                print("\nGoodbye!")
                return
            except Exception as e:
                self.logger.error(f"Unexpected error in admin menu: {e}")
                self.display_error("An unexpected error occurred. Please try again.")

    def _get_menu_choice(self) -> str:
        print("[1] View External Servers")
        print("[2] Update Server API Key")
        print("[3] Add Category")
        print("[4] View Reported Articles")
        print("[5] Hide Category")
        print("[6] Blacklist Keyword")
        print("[7] Logout")
        return input("Choice: ").strip()

    def _handle_view_servers(self) -> None:
        try:
            servers = self.admin_service.get_external_servers()

            print("\nExternal Server Status:")
            for server in servers:
                name = server["name"]
                status = "Active" if server.get("is_active") else "Inactive"
                last_accessed = server.get("last_accessed")

                if last_accessed:
                    try:
                        last_accessed = datetime.fromisoformat(last_accessed).strftime(
                            "%Y-%m-%d %H:%M"
                        )
                    except ValueError:
                        last_accessed = "Invalid date"
                else:
                    last_accessed = "Never"

                print(f"- {name}: {status} | Last accessed: {last_accessed}")

        except DataProcessingError as e:
            self.display_error(str(e))
        except Exception as e:
            self.logger.error(f"Error viewing server status: {e}")
            self.display_error("Failed to fetch external servers")

        self.pause()

    def _handle_update_server(self) -> None:
        try:
            server_id = self.get_user_input("Enter server ID: ")
            if not server_id:
                self.display_error("Server ID cannot be empty.")
                return

            api_key = self.get_user_input("Enter updated API key: ")
            if not api_key:
                self.display_error("API key cannot be empty.")
                return

            self.admin_service.update_external_server(server_id, api_key)
            self.display_success("API key updated successfully.")

        except DataProcessingError as e:
            self.display_error(str(e))
        except Exception as e:
            self.logger.error(f"Error updating server: {e}")
            self.display_error("Failed to update external server")

        self.pause()

    def _handle_add_category(self) -> None:
        try:
            name = self.get_user_input("Enter new category name: ")
            if not name:
                self.display_error("Category name cannot be empty.")
                return

            self.admin_service.add_category(name)
            self.display_success("Category added successfully.")

        except DataProcessingError as e:
            self.display_error(str(e))
        except Exception as e:
            self.logger.error(f"Error adding category: {e}")
            self.display_error("Failed to add category")

        self.pause()

    def _handle_view_reports(self) -> None:
        try:
            reports = self.admin_service.get_reported_articles()

            if not reports:
                self.display_info("No reported articles.")
                return

            print("\nReported Articles:")
            for report in reports:
                print(f"Report ID: {report['id']}, Article ID: {report['article_id']}")

            article_id = self.get_user_input(
                "Enter article ID to hide or press Enter to skip: ", required=False
            )
            if article_id:
                if self.confirm_action(
                    f"Are you sure you want to hide article {article_id}? (y/n): "
                ):
                    self.admin_service.hide_article(article_id)
                    self.display_success("Article hidden successfully.")

        except DataProcessingError as e:
            self.display_error(str(e))
        except Exception as e:
            self.logger.error(f"Error viewing reported articles: {e}")
            self.display_error("Failed to fetch reports")

    def _handle_hide_category(self) -> None:
        try:
            category_name_input = self.get_user_input("Enter category name to hide: ")
            if not category_name_input:
                self.display_error("Category name is required.")
                return
            category_name = category_name_input.strip().lower()

            categories = self.admin_service.get_categories()
            matching = next(
                (c for c in categories if c["name"].lower() == category_name), None
            )

            if not matching:
                self.display_error(f"Category '{category_name}' not found.")
                return

            category_id = matching["id"]

            if self.confirm_action(
                f"Are you sure you want to hide category '{matching['name']}'? (y/n): "
            ):
                self.admin_service.hide_category(category_id)
                self.display_success("Category hidden successfully.")

        except DataProcessingError as e:
            self.display_error(str(e))
        except Exception as e:
            self.logger.error(f"Error hiding category: {e}")
            self.display_error("Failed to hide category")

    def _handle_blacklist_keyword(self) -> None:
        try:
            keyword_input = self.get_user_input("Enter keyword to blacklist: ")
            if not keyword_input:
                self.display_error("Keyword is required.")
                return
            keyword = keyword_input.strip().lower()

            if self.confirm_action(
                f"Are you sure you want to blacklist '{keyword}'? (y/n): "
            ):
                self.admin_service.blacklist_keyword(keyword)
                self.display_success("Keyword blacklisted successfully.")

        except DataProcessingError as e:
            self.display_error(str(e))
        except Exception as e:
            self.logger.error(f"Error blacklisting keyword: {e}")
            self.display_error("Failed to blacklist keyword")
