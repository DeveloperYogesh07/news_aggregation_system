import requests
from ui.base_menu import BaseMenu
from datetime import datetime


class AdminMenu(BaseMenu):
    def __init__(self, api_client):
        super().__init__()
        self.api_client = api_client

    def show(self):
        while True:
            self.print_header("Admin Menu")
            choice = input(
                "[1] View External Servers Status\n"
                "[2] View External Servers Details\n"
                "[3] Update/Edit External Server API Key\n"
                "[4] Add New News Category\n"
                "[5] View Reported Articles\n"
                "[6] Hide Category\n"
                "[7] Blacklist Keyword\n"
                "[8] Logout\nChoice: "
            ).strip()

            if choice == "1":
                self.view_external_server_status()
            elif choice == "2":
                self.view_external_server_details()
            elif choice == "3":
                self.update_external_server()
            elif choice == "4":
                self.add_news_category()
            elif choice == "5":
                self.view_reported_articles()
            elif choice == "6":
                self.hide_category()
            elif choice == "7":
                self.blacklist_keyword()
            elif choice == "8":
                print("Logging out...")
                exit()
            else:
                print("Invalid choice. Please try again.")

    def view_external_server_status(self):
        try:
            servers = self.api_client.get("/admin/external-sources")
            print("\nExternal Server Status:")
            for server in servers:
                name = server["name"]
                status = "Active" if server.get("is_active") else " Inactive"
                last_accessed = server.get("last_accessed")
                if last_accessed:
                    try:
                        last_accessed = datetime.fromisoformat(last_accessed).strftime(
                            "%Y-%m-%d %H:%M"
                        )
                    except ValueError:
                        pass
                else:
                    last_accessed = "Never"
                print(f"- {name}: {status} | Last accessed: {last_accessed}")
        except Exception as e:
            print(f"Failed to fetch external servers: {e}")
        self.pause()

    def view_external_server_details(self):
        try:
            details = self.api_client.get("/admin/external-sources")
            print("\nExternal Server Details:")
            for detail in details:
                name = detail["name"]
                api_key = detail.get("api_key") or "<None>"
                print(f"- {name}: API Key: {api_key}")
        except Exception as e:
            print(f"Failed to fetch external server details: {e}")
        self.pause()

    def update_external_server(self):
        try:
            server_id = input("Enter server ID: ").strip()
            if not server_id:
                print("Server ID cannot be empty.")
                return
            api_key = input("Enter updated API key: ").strip()
            if not api_key:
                print("API key cannot be empty.")
                return
            self.api_client.put(
                f"/admin/external-sources/{server_id}", {"api_key": api_key}
            )
            print("API key updated successfully.")
        except requests.exceptions.HTTPError as http_err:
            try:
                detail = http_err.response.json().get("detail")
                print(f"Failed to update: {detail}")
            except Exception:
                print(f"HTTP error: {http_err}")
        except Exception as e:
            print(f"Failed to update external server: {e}")
        self.pause()

    def add_news_category(self):
        try:
            name = input("Enter new category name: ").strip()
            if not name:
                print("Category name cannot be empty.")
                return
            self.api_client.post("/admin/categories/", {"name": name})
            print("Category added successfully.")
        except requests.exceptions.HTTPError as http_err:
            try:
                detail = http_err.response.json().get("detail")
                print(f"Failed to add category: {detail}")
            except Exception:
                print(f"HTTP error: {http_err}")
        except Exception as e:
            print(f"Unexpected error: {e}")
        self.pause()

    def pause(self):
        input("\nPress Enter to return to the menu...")

    def view_reported_articles(self):
        try:
            reports = self.api_client.get("/admin/reported-articles")
            if not reports:
                print("No reported articles.")
                return

            print("\nReported Articles:")
            for report in reports:
                print(f"Report ID: {report['id']}, Article ID: {report['article_id']}")
            choice = input("Enter article ID to hide or press Enter to skip: ").strip()
            if choice:
                self.api_client.put(f"/admin/articles/{choice}/hide", data={})
                print("Article hidden.")
        except Exception as e:
            print(f"Failed to fetch reports: {e}")

    def hide_category(self):
        name = input("Enter category name to hide: ").strip().lower()
        if not name:
            print("Category name is required.")
            return
        try:
            # First fetch all categories
            categories = self.api_client.get("/categories/")
            matching = next((c for c in categories if c["name"].lower() == name), None)
            if not matching:
                print(f"Category '{name}' not found.")
                return

            category_id = matching["id"]

            # Now make the PUT request with category ID
            self.api_client.put(f"/admin/categories/{category_id}/hide",data={})
            print("Category hidden successfully.")
        except Exception as e:
            print(f"Failed to hide category: {e}")


    def blacklist_keyword(self):
        keyword = input("Enter keyword to blacklist: ").strip().lower()
        if not keyword:
            print("Keyword is required.")
            return
        try:
            self.api_client.post("/admin/blacklist-keyword", {"keyword": keyword})
            print("Keyword blacklisted.")
        except Exception as e:
            print(f"Failed to blacklist keyword: {e}")
