import logging
from typing import Optional, Dict, Any, List
from datetime import datetime, date
from ui.base_menu import BaseMenu
from services.api_client import APIClient
from exceptions.custom_exceptions import (
    AuthenticationError,
    NetworkError,
    DataProcessingError,
)
from ui.notification import NotificationMenu


class UserService:

    def __init__(self, api_client: APIClient):
        self.api_client = api_client
        self.logger = logging.getLogger(__name__)

    def get_articles_by_date(
        self, target_date: date, category: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        try:
            params = {"date": str(target_date)}
            if category:
                params["category"] = category

            response = self.api_client.get("/articles/", params=params)
            return response.get("data", []) if isinstance(response, dict) else response

        except Exception as e:
            self.logger.error(f"Failed to fetch articles for date {target_date}: {e}")
            raise DataProcessingError(
                "fetch articles by date", f"Failed to fetch articles: {e}"
            )

    def get_articles_by_range(
        self, start_date: str, end_date: str, category: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        try:
            params = {"start_date": start_date, "end_date": end_date}
            if category:
                params["category"] = category

            response = self.api_client.get("/articles/range", params=params)
            return response.get("data", []) if isinstance(response, dict) else response

        except Exception as e:
            self.logger.error(
                f"Failed to fetch articles for range {start_date} to {end_date}: {e}"
            )
            raise DataProcessingError(
                "fetch articles by range", f"Failed to fetch articles: {e}"
            )

    def get_categories(self) -> List[Dict[str, Any]]:
        try:
            response = self.api_client.get_categories()
            return response.get("data", []) if isinstance(response, dict) else response

        except Exception as e:
            self.logger.error(f"Failed to fetch categories: {e}")
            raise DataProcessingError(
                "fetch categories", f"Failed to fetch categories: {e}"
            )

    def get_saved_articles(self) -> List[Dict[str, Any]]:
        try:
            response = self.api_client.get("/saved-articles/")
            return response.get("data", []) if isinstance(response, dict) else response

        except Exception as e:
            self.logger.error(f"Failed to fetch saved articles: {e}")
            raise DataProcessingError(
                "fetch saved articles", f"Failed to fetch saved articles: {e}"
            )

    def search_articles(self, query: str) -> List[Dict[str, Any]]:
        try:
            response = self.api_client.get("/articles/search", params={"query": query})
            return response.get("data", []) if isinstance(response, dict) else response

        except Exception as e:
            self.logger.error(f"Failed to search articles with query '{query}': {e}")
            raise DataProcessingError(
                "search articles", f"Failed to search articles: {e}"
            )

    def save_article(self, article: Dict[str, Any]) -> None:
        try:
            payload = {
                "article_id": article["id"],
                "title": article["title"],
                "content": article.get("content", ""),
                "url": article.get("url") or None,
            }
            self.api_client.post("/saved-articles/", payload)

        except Exception as e:
            self.logger.error(f"Failed to save article {article.get('id')}: {e}")
            raise DataProcessingError("save article", f"Failed to save article: {e}")

    def vote_article(self, article_id: int, vote_type: str) -> None:
        try:
            payload = {"article_id": article_id, "vote": vote_type}
            self.api_client.post("/votes/", data=payload)

        except Exception as e:
            self.logger.error(
                f"Failed to vote {vote_type} on article {article_id}: {e}"
            )
            raise DataProcessingError("vote article", f"Failed to vote on article: {e}")

    def report_article(self, article_id: int) -> None:
        try:
            self.api_client.post(f"/articles/report/{article_id}")

        except Exception as e:
            self.logger.error(f"Failed to report article {article_id}: {e}")
            raise DataProcessingError(
                "report article", f"Failed to report article: {e}"
            )


class UserMenu(BaseMenu):
    pass

    def __init__(self, api_client: APIClient):
        super().__init__()
        self.user_service = UserService(api_client)
        self.last_displayed_articles: List[Dict[str, Any]] = []

    def show(self) -> None:
        while True:
            try:
                self.print_header("User Menu")
                choice = self._get_menu_choice()

                if choice == "1":
                    self._handle_headlines()
                elif choice == "2":
                    self._handle_saved_articles()
                elif choice == "3":
                    self._handle_search()
                elif choice == "4":
                    NotificationMenu(self.user_service.api_client).show()
                elif choice == "5":
                    self.display_info("Logging out...")
                    return
                else:
                    self.display_error("Invalid choice. Please try again.")

            except KeyboardInterrupt:
                print("\nGoodbye!")
                return
            except Exception as e:
                self.logger.error(f"Unexpected error in user menu: {e}")
                self.display_error("An unexpected error occurred. Please try again.")

    def _get_menu_choice(self) -> str:
        print("[1] Headlines")
        print("[2] Saved Articles")
        print("[3] Search")
        print("[4] Notifications")
        print("[5] Logout")
        return input("Choice: ").strip()

    def _handle_headlines(self) -> None:
        while True:
            try:
                self.print_header("H E A D L I N E S")
                print("Please choose the options below")
                print("[1] Today")
                print("[2] Date range")
                print("[3] Back")

                choice = input("Choice: ").strip()
                if choice == "1":
                    self._handle_today_headlines()
                elif choice == "2":
                    self._handle_date_range_headlines()
                elif choice == "3":
                    return
                else:
                    self.display_error("Invalid choice.")

            except KeyboardInterrupt:
                return
            except Exception as e:
                self.logger.error(f"Error in headlines menu: {e}")
                self.display_error("An error occurred. Please try again.")

    def _handle_today_headlines(self) -> None:
        try:
            articles = self.user_service.get_articles_by_date(datetime.today().date())
            if not articles:
                self.display_info("No articles found for today.")
                return

            self.last_displayed_articles = articles
            self._display_articles()

        except DataProcessingError as e:
            self.display_error(str(e))
        except Exception as e:
            self.logger.error(f"Error fetching today's headlines: {e}")
            self.display_error("Failed to fetch today's headlines")

    def _handle_date_range_headlines(self) -> None:
        try:
            start_date = self.get_user_input("Enter start date (YYYY-MM-DD): ")
            if not start_date:
                self.display_error("Start date is required.")
                return

            end_date = self.get_user_input("Enter end date (YYYY-MM-DD): ")
            if not end_date:
                self.display_error("End date is required.")
                return

            categories = self.user_service.get_categories()
            print("\nPlease choose the options below for Headlines")
            print("[1] All")

            category_map = {"1": None}
            for idx, cat in enumerate(categories, start=2):
                print(f"[{idx}] {cat['name'].capitalize()}")
                category_map[str(idx)] = cat["name"]

            choice = input("Choice: ").strip()
            category = category_map.get(choice)

            if choice not in category_map:
                self.display_error("Invalid choice.")
                return

            articles = self.user_service.get_articles_by_range(
                start_date, end_date, category
            )
            if not articles:
                self.display_info("No articles found for the selected date range.")
                return

            self.last_displayed_articles = articles
            self._display_articles()

        except DataProcessingError as e:
            self.display_error(str(e))
        except Exception as e:
            self.logger.error(f"Error fetching date range headlines: {e}")
            self.display_error("Failed to fetch headlines for date range")

    def _display_articles(self) -> None:
        print("\nH E A D L I N E S")
        for article in self.last_displayed_articles:
            print(f"ID: {article['id']}\nTitle: {article['title']}\n{'-' * 40}")
        self._handle_article_selection()

    def _handle_article_selection(self) -> None:
        article_id_input = self.get_user_input(
            "Enter the Article ID to view full content: "
        )
        if not article_id_input:
            return

        article = next(
            (
                a
                for a in self.last_displayed_articles
                if str(a["id"]) == article_id_input
            ),
            None,
        )

        if not article:
            self.display_error("Article not found.")
            return

        self._display_article_details(article)
        self._handle_article_interaction(article)

    def _display_article_details(self, article: Dict[str, Any]) -> None:
        print(f"\nTitle: {article['title']}")
        print(f"Content: {article.get('content', '[No content]')}")
        print(f"URL: {article.get('url', '-')}")
        self.print_separator()

    def _handle_article_interaction(self, article: Dict[str, Any]) -> None:
        while True:
            try:
                print("1. Back")
                print("2. Save Article")
                print("3. Like")
                print("4. Dislike")
                print("5. Report Article")

                choice = input("Choice: ").strip()

                if choice == "1":
                    return
                elif choice == "2":
                    self._handle_save_article(article)
                    break
                elif choice == "3":
                    self._handle_vote_article(article["id"], "like")
                    break
                elif choice == "4":
                    self._handle_vote_article(article["id"], "dislike")
                    break
                elif choice == "5":
                    self._handle_report_article(article["id"])
                    break
                else:
                    self.display_error("Invalid choice.")

            except KeyboardInterrupt:
                return
            except Exception as e:
                self.logger.error(f"Error in article interaction: {e}")
                self.display_error("An error occurred. Please try again.")

    def _handle_save_article(self, article: Dict[str, Any]) -> None:
        try:
            self.user_service.save_article(article)
            self.display_success("Article saved successfully.")
        except DataProcessingError as e:
            self.display_error(str(e))
        except Exception as e:
            self.logger.error(f"Error saving article: {e}")
            self.display_error("Failed to save article")

    def _handle_vote_article(self, article_id: int, vote_type: str) -> None:
        try:
            self.user_service.vote_article(article_id, vote_type)
            self.display_success(f"You {vote_type}d this article.")
        except DataProcessingError as e:
            self.display_error(str(e))
        except Exception as e:
            self.logger.error(f"Error voting on article: {e}")
            self.display_error(f"Failed to {vote_type} article")

    def _handle_report_article(self, article_id: int) -> None:
        try:
            self.user_service.report_article(article_id)
            self.display_success("Article reported successfully.")
        except DataProcessingError as e:
            self.display_error(str(e))
        except Exception as e:
            self.logger.error(f"Error reporting article: {e}")
            self.display_error("Failed to report article")

    def _handle_saved_articles(self) -> None:
        try:
            saved = self.user_service.get_saved_articles()
            if not saved:
                self.display_info("You haven't saved any articles.")
                return

            print("\nSaved Articles:")
            for article in saved:
                print(
                    f"ID: {article['article_id']}\nTitle: {article['title']}\n{'-' * 40}"
                )

        except DataProcessingError as e:
            self.display_error(str(e))
        except Exception as e:
            self.logger.error(f"Error viewing saved articles: {e}")
            self.display_error("Failed to fetch saved articles")

    def _handle_search(self) -> None:
        try:
            query = self.get_user_input("Enter keyword to search: ")
            if not query:
                self.display_error("Query cannot be empty.")
                return

            articles = self.user_service.search_articles(query)
            if not articles:
                self.display_info("No articles found matching your search.")
                return

            self.last_displayed_articles = articles
            print("\nSearch Results:")
            for article in articles:
                print(f"ID: {article['id']}\nTitle: {article['title']}\n{'-' * 40}")

            self._handle_article_selection()

        except DataProcessingError as e:
            self.display_error(str(e))
        except Exception as e:
            self.logger.error(f"Error searching articles: {e}")
            self.display_error("Search failed")
