from ui.base_menu import BaseMenu

class AdminMenu(BaseMenu):
    def __init__(self, api_client):
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
                break
            else:
                print("Invalid choice.")

    def view_external_server_status(self):
        try:
            sources = self.api_client.get("/admin/external-sources/")
            print("\nList of external servers:")
            for idx, source in enumerate(sources, start=1):
                last_accessed = source.get("last_accessed") or "Never"
                status = "Active" if source.get("is_active") else "Not Active"
                print(f"{idx}. {source['name']} - {status} - Last accessed: {last_accessed}")
        except Exception as e:
            print(f"Failed to fetch external servers: {e}")

    def view_external_server_details(self):
        try:
            sources = self.api_client.get("/admin/external-sources/")
            print("\nList of external server details:")
            for idx, source in enumerate(sources, start=1):
                print(f"{idx}. {source['name']} - API Key: {source.get('api_key') or '<None>'}")
        except Exception as e:
            print(f"Failed to fetch external server details: {e}")

    def update_external_server(self):
        try:
            sources = self.api_client.get("/admin/external-sources/")
            for s in sources:
                print(f"[{s['id']}] {s['name']}")

            ext_id = int(input("Enter the external server ID: "))
            updated_api_key = input("Enter the updated API key: ")
            self.api_client.put(f"/admin/external-sources/{ext_id}", {"api_key": updated_api_key})
            print("External server updated successfully.")
        except Exception as e:
            print(f"Failed to update external server: {e}")

    def add_news_category(self):
        try:
            name = input("Enter new category name: ").strip()
            if not name:
                print("Category name cannot be empty.")
                return
            self.api_client.post("/admin/categories/", {"name": name})
            print("Category added successfully.")
        except Exception as e:
            print(f"Failed to add category: {e}")
