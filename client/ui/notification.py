from ui.base_menu import BaseMenu
from datetime import datetime

class NotificationMenu(BaseMenu):
    def __init__(self, api_client):
        super().__init__()
        self.api_client = api_client

    def show(self):
        while True:
            self.print_header("N O T I F I C A T I O N S")
            print(f"Welcome to News Application! Date: {datetime.now().strftime('%d-%b-%Y')}")
            print(f"Time: {datetime.now().strftime('%I:%M %p')}")
            choice = input("\n1. View Notifications\n2. Configure Notifications\n3. Back\n4. Logout\nChoice: ")

            if choice == "1":
                self._view_notifications()
            elif choice == "2":
                self.configure()
            elif choice == "3":
                break
            elif choice == "4":
                exit()
            else:
                print("Invalid choice.")

    def _view_notifications(self):
        try:
            notices = self.api_client.get("/notifications/history")
            if not notices:
                print("\nNo notifications yet.")
                input("Press Enter to continue...")
                return
            print("\nNotifications:")
            for n in notices:
                print(f"- [{n['created_at']}] {n['message']}")
            input("\nPress Enter to continue...")
        except Exception as e:
            print(f"Failed to fetch notifications: {e}")
            input("Press Enter to continue...")

    def configure(self):
        try:
            configs = self.api_client.get("/notifications/")
            if not configs:
                print("No notification configurations found.")
                return

            while True:
                self.print_header("C O N F I G U R E - N O T I F I C A T I O N S")
                mapping = {}
                for idx, config in enumerate(configs, 1):
                    label = config["category"] or "Keywords"
                    status = "Enabled" if config["enabled"] else "Disabled"
                    print(f"{idx}. {label} - {status}")
                    mapping[str(idx)] = config

                print(f"{len(configs)+1}. Back")
                print(f"{len(configs)+2}. Logout")

                option = input("Enter your option: ").strip()

                if option == str(len(configs) + 1):
                    break
                elif option == str(len(configs) + 2):
                    exit()
                elif option in mapping:
                    selected = mapping[option]
                    self.toggle_notification(selected)
                else:
                    print("Invalid option.")

        except Exception as e:
            print(f"Failed to load config: {e}")
            input("Press Enter to continue...")

    def toggle_notification(self, config):
        try:
            if config["category"]:
                # Toggle category
                new_value = not config["enabled"]
                self.api_client.put(f"/notifications/{config['id']}", {"enabled": new_value})
                print(f"{config['category']} notification {'enabled' if new_value else 'disabled'}.")
            else:
                # Keyword update
                new_keywords = input("Enter comma-separated keywords: ").strip()
                if not new_keywords:
                    print("Keyword list cannot be empty.")
                    return
                keywords = [k.strip() for k in new_keywords.split(",") if k.strip()]
                self.api_client.put("/notifications/keywords", {"keywords": keywords})
                print("Keywords updated.")
        except Exception as e:
            print(f"Update failed: {e}")
        input("Press Enter to continue...")
