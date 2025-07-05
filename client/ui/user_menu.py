import datetime
from ui.base_menu import BaseMenu
import requests
from ui.notification import NotificationMenu

class UserMenu(BaseMenu):
    def __init__(self, api_client):
        super().__init__()
        self.api_client = api_client
        self.last_displayed_articles = []

    def show(self):
        while True:
            self.print_header("User Menu")
            choice = input(
                "[1] Headlines\n"
                "[2] Saved Articles\n"
                "[3] Search\n"
                "[4] Notifications\n"
                "[5] Logout\nChoice: "
            )

            if choice == "1":
                self.view_headlines()
            elif choice == "2":
                self.view_saved_articles()
            elif choice == "3":
                self.search_articles()
            elif choice == "4":
                NotificationMenu(self.api_client).show()  
            elif choice == "5": 
                print("Logging out...")
                break
            else:
                print("Invalid choice.")

    def view_headlines(self):
        while True:
            self.print_header("H E A D L I N E S")
            print("Please choose the options below")
            print("[1] Today")
            print("[2] Date range")
            print("[3] Logout")

            choice = input("Choice: ").strip()
            if choice == "1":
                self._fetch_articles_by_date(datetime.datetime.today().date())
            elif choice == "2":
                self._date_range_menu()
            elif choice == "3":
                break
            else:
                print("Invalid choice.")

    
    def _fetch_articles_by_date(self, date, category=None):
        params = {"date": str(date)}
        if category:
            params["category"] = category

        try:
            articles = self.api_client.get("/articles/", params=params)
            if not articles:
                print("No articles found.")
                return

            self.last_displayed_articles = articles
            print("\nH E A D L I N E S")
            for article in articles:
                print(f"ID: {article['id']}\nTitle: {article['title']}\n{'-'*40}")
            self.select_article_menu()
        except Exception as e:
            print(f"Error: {e}")


    def _date_range_menu(self):
        try:
            start_date = input("Enter start date (YYYY-MM-DD): ").strip()
            end_date = input("Enter end date (YYYY-MM-DD): ").strip()

            # Fetch categories from backend
            categories = self.api_client.get_categories()

            print("\nPlease choose the options below for Headlines")
            print("[1] All")

            category_map = {"1": None}
            for idx, cat in enumerate(categories, start=2):
                print(f"[{idx}] {cat['name'].capitalize()}")
                category_map[str(idx)] = cat["name"]

            choice = input("Choice: ").strip()
            category = category_map.get(choice)

            if choice not in category_map:
                print("Invalid choice.")
                return

            self._fetch_articles_by_range(start_date, end_date, category)

        except Exception as e:
            print(f"Error: {e}")


        except Exception as e:
            print(f"Error: {e}")


    def _fetch_articles_by_range(self, start_date, end_date, category=None):
        params = {"start_date": start_date, "end_date": end_date}
        if category:
            params["category"] = category

        try:
            articles = self.api_client.get("/articles/range", params=params)
            if not articles:
                print("No articles found.")
                return

            self.last_displayed_articles = articles
            print("\nH E A D L I N E S")
            for article in articles:
                print(f"ID: {article['id']}\nTitle: {article['title']}\n{'-'*40}")
            self.select_article_menu()
        except Exception as e:
            print(f"Error: {e}")

    def view_saved_articles(self):
        try:
            saved = self.api_client.get("/saved-articles/")
            if not saved:
                print("You haven't saved any articles.")
                return

            print("\nSaved Articles:")
            for article in saved:
                print(f"ID: {article['article_id']}\nTitle: {article['title']}\n" + "-" * 40)
        except Exception as e:
            print(f"Failed to fetch saved articles: {e}")

    def search_articles(self):
        try:
            query = input("Enter keyword to search: ").strip()
            if not query:
                print("Query cannot be empty.")
                return

            articles = self.api_client.get("/articles/search", params={"query": query})

            if not articles:
                print("No articles found matching your search.")
                return

            self.last_displayed_articles = articles
            print("\nSearch Results:")
            for article in articles:
                print(f"ID: {article['id']}\nTitle: {article['title']}\n" + "-" * 40)

            self.select_article_menu()

        except Exception as e:
            print(f"Search failed: {e}")


    def select_article_menu(self):
        article_id = input("Enter the Article ID to view full content: ").strip()
        article = next((a for a in self.last_displayed_articles if str(a["id"]) == article_id), None)

        if not article:
            print("Article not found.")
            return

        print(f"\nTitle: {article['title']}")
        print(f"Content: {article.get('content', '[No content]')}")
        print(f"URL: {article.get('url', '-')}")
        print("-" * 40)

        while True:
            choice = input("1. Back\n2. Logout\n3. Save Article\nChoice: ")

            if choice == "1":
                break
            elif choice == "2":
                exit()
            elif choice == "3":
                self.save_article(article)
                break
            else:
                print("Invalid choice.")

    def save_article(self, article):
        try:
            payload = {
                "article_id": article["id"],
                "title": article["title"],
                "content": article.get("content", ""),
                "url": article.get("url") or None
            }
            self.api_client.post("/saved-articles/", payload)
            print("Article saved successfully.")
        except requests.exceptions.HTTPError as err:
            try:
                error_data = err.response.json()
                print("Save failed:", error_data.get("detail"))
            except:
                print("Save failed:", err)
        except Exception as e:
            print(f"Error: {e}")
