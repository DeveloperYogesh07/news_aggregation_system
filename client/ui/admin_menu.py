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
                "[5] Logout\nChoice: "
            )
            if choice == "1":
                self.view_external_server_status()
            elif choice == "2":
                self.view_external_server_details()
            elif choice == "3":
                self.update_external_server()
            elif choice == "4":
                self.add_news_category()
            elif choice == "5":
                print("Logging out...")
                break
            else:
                print("Invalid choice. Please try again.")

    def view_external_server_status(self):
        try:
            result = self.api_client.get("/admin/external-sources")
            if "error" in result:
                print(result["error"])
            else:
                # servers = result.get("servers", [])
                print("\nExternal Server Status:")
                for server in result:
                    name = server["name"]
                    status = "Active" if server.get("is_active") else "Not Active"
                    last_accessed = server.get("last_accessed")
                    if last_accessed:
                        try:
                            last_accessed = datetime.fromisoformat(last_accessed).strftime("%Y-%m-%d %H:%M")
                        except Exception:
                            pass
                    else:
                        last_accessed = "Never"

                    print(f"- {name}: {status} - Last accessed: {last_accessed}")
        except Exception as e:
            print(f"Failed to fetch external servers: {e}")
        input("\nPress Enter to continue...")

    def view_external_server_details(self):
        try:
            result = self.api_client.get("/admin/external-sources")
            if "error" in result:
                print(result["error"])
            else:
                # details = result.get("details", [])
                print("\nExternal Server Details:")
                for detail in result:
                    name = detail["name"]
                    api_key = detail.get("api_key") or "<None>"
                    print(f"- {name}: API Key: {api_key}")
        except Exception as e:
            print(f"Failed to fetch external server details: {e}")
        input("\nPress Enter to continue...")

    def update_external_server(self):
        try:
            server_id = input("Enter server ID: ").strip()
            api_key = input("Enter updated API key: ").strip()
            result = self.api_client.put(f"/admin/external-sources/{server_id}", {"api_key": api_key})
            if "error" in result:
                print(result["error"])
            else:
                print("API key updated successfully.")
        except Exception as e:
            print(f"Failed to update external server: {e}")
        input("\nPress Enter to continue...")

    def add_news_category(self):
        try:
            name = input("Enter new category name: ").strip()
            if not name:
                print("Category name cannot be empty.")
                return
            result = self.api_client.post("/admin/categories/", {"name": name})
            print("Category added successfully.")
        except requests.exceptions.HTTPError as http_err:
            try:
                error_response = http_err.response.json()
                print(f"Failed to add category: {error_response.get('detail')}")
            except Exception:
                print(f"Failed to add category: {http_err}")
        except Exception as e:
            print(f"Unexpected error: {e}")
        input("\nPress Enter to continue...")

