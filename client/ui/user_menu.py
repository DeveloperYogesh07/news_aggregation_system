from ui.base_menu import BaseMenu


class UserMenu(BaseMenu):
    def __init__(self, api_client):
        self.api_client = api_client

    def show(self):
        while True:
            self.print_header("User Menu")
            choice = input("[1] View Articles\n[0] Logout\nChoice: ")
            if choice == "1":
                self.view_articles()
            elif choice == "0":
                break
            else:
                print("Invalid choice.")

    def view_articles(self):
        try:
            articles = self.api_client.get("/articles/")
            for article in articles:
                print(
                    f"\nTitle: {article['title']}\nContent: {article['content']}\n{'-'*40}"
                )
        except Exception as e:
            print(f"Failed to fetch articles: {e}")
