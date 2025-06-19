from ui.base_menu import BaseMenu

class AdminMenu(BaseMenu):
    def __init__(self, api_client):
        self.api_client = api_client

    def show(self):
        while True:
            self.print_header("Admin Menu")
            choice = input(
                "[1] Fetch External News\n"
                "[2] List External Sources\n"
                "[3] Add External Source\n"
                "[4] Delete External Source\n"
                "[0] Logout\nChoice: "
            )
            if choice == "1":
                self.fetch_external_news()
            elif choice == "2":
                self.list_external_sources()
            elif choice == "3":
                self.add_external_source()
            elif choice == "4":
                self.delete_external_source()
            elif choice == "0":
                break
            else:
                print("Invalid choice.")

    def fetch_external_news(self):
        try:
            self.api_client.post("/articles/fetch-external")
            print("External news fetched successfully.")
        except Exception as e:
            print(f"Error fetching news: {e}")

    def list_external_sources(self):
        try:
            sources = self.api_client.get("/admin/external-sources/")
            for s in sources:
                print(f"[{s['id']}] {s['name']} → {s['base_url']} → Active: {s['is_active']}")
        except Exception as e:
            print(f"Failed to list sources: {e}")

    def add_external_source(self):
        name = input("Name: ")
        base_url = input("Base URL: ")
        api_key = input("API Key (if any, leave empty for none): ")
        is_active = input("Active (y/n): ").lower() == "y"
        try:
            self.api_client.post("/admin/external-sources/", {
                "name": name,
                "base_url": base_url,
                "api_key": api_key or None,
                "is_active": is_active
            })
            print(" External source added.")
        except Exception as e:
            print(f" Failed to add source: {e}")

    def delete_external_source(self):
        try:
            source_id = int(input("Enter Source ID to delete: "))
            self.api_client.delete(f"/admin/external-sources/{source_id}")
            print("External source deleted.")
        except Exception as e:
            print(f" Failed to delete source: {e}")
