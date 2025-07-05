from ui.base_menu import BaseMenu

class NotificationMenu(BaseMenu):
    def __init__(self, api_client):
        self.api_client = api_client

    def show(self):
        while True:
            self.print_header("NOTIFICATIONS")
            choice = input("1. View Notifications\n2. Configure Notifications\n3. Back\n4. Logout\nChoice: ")

            if choice == "1":
                self.view_notifications()
            elif choice == "2":
                self.configure_notifications()
            elif choice == "3":
                break
            elif choice == "4":
                exit()
            else:
                print("Invalid choice.")

    def view_notifications(self):
        try:
            configs = self.api_client.get("/notifications/")
            print("\nYour Notification Configurations:")
            for cfg in configs:
                label = cfg["category"] or f"Keyword: {cfg['keyword']}"
                status = "Enabled" if cfg["enabled"] else "Disabled"
                print(f"{cfg['id']}. {label} - {status}")
        except Exception as e:
            print(f"Error: {e}")

    def configure_notifications(self):
        try:
            configs = self.api_client.get("/notifications/")
            while True:
                print("\nC O N F I G U R E  -  N O T I F I C A T I O N S")
                for cfg in configs:
                    label = cfg["category"] or f"Keyword: {cfg['keyword']}"
                    status = "Enabled" if cfg["enabled"] else "Disabled"
                    print(f"{cfg['id']}. {label} - {status}")
                print("K. Set Keywords\nB. Back\nL. Logout")

                choice = input("Enter option to toggle (ID), or command: ").strip().lower()
                if choice == "b":
                    break
                elif choice == "l":
                    exit()
                elif choice == "k":
                    keywords = input("Enter comma-separated keywords: ").strip().split(",")
                    cleaned = [kw.strip() for kw in keywords if kw.strip()]
                    self.api_client.put("/notifications/keywords", cleaned)
                    print("Keywords updated.")
                elif choice.isdigit():
                    config_id = int(choice)
                    config = next((c for c in configs if c["id"] == config_id), None)
                    if config:
                        self.api_client.put(f"/notifications/{config_id}", data={"enabled": not config["enabled"]})
                        print("Toggled status.")
                        configs = self.api_client.get("/notifications/") 
                    else:
                        print("Invalid ID.")
                else:
                    print("Invalid option.")
        except Exception as e:
            print(f"Failed to configure notifications: {e}")
