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
            result = self.api_client.get("/admin/external-sources/status")
            if "error" in result:
                print(result["error"])
            else:
                servers = result.get("servers", [])
                for server in servers:
                    print(f"{server['name']} - {'Active' if server.get('is_active') else 'Not Active'} - Last accessed: {server.get('last_accessed') or 'Never'}")
        except Exception as e:
            print({"error": f"Failed to fetch external servers: {e}"})
        input("Press Enter to continue...")

def view_external_server_details(self):
    """Display external servers details (logic same as AdminInterface.show_server_details)"""
    try:
        result = self.api_client.get("/admin/external-sources/details")
        if "error" in result:
            print(result["error"])
        else:
            details = result.get("details", [])
            for detail in details:
                print(f"{detail['name']} - API Key: {detail.get('api_key') or '<None>'}")
    except Exception as e:
        print({"error": f"Failed to fetch external server details: {e}"})
    input("Press Enter to continue...")

def update_external_server(self):
    """Update external server API key (logic same as AdminInterface.handle_update_server)"""
    try:
        server_id = input("Enter server ID: ")
        api_key = input("Enter updated API key: ")
        result = self.api_client.put(f"/admin/external-sources/{server_id}", {"api_key": api_key})
        print(result)
    except Exception as e:
        print({"error": f"Failed to update external server: {e}"})
    input("Press Enter to continue...")

def add_news_category(self):
    """Add new category (logic same as AdminInterface.handle_add_category)"""
    try:
        name = input("Enter new category name: ").strip()
        result = self.api_client.post("/admin/categories/", {"name": name})
        print(result)
    except Exception as e:
        print({"error": f"Failed to add category: {e}"})
    input("Press Enter to continue...")

