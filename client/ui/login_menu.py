import logging
from typing import Optional, Dict, Any
from ui.base_menu import BaseMenu
from services.api_client import APIClient
from exceptions.custom_exceptions import (
    AuthenticationError,
    NetworkError,
    DataProcessingError,
)
from utils.validators import validate_email, validate_password, validate_username


class AuthenticationService:

    def __init__(self, api_client: APIClient):
        self.api_client = api_client
        self.logger = logging.getLogger(__name__)

    def login(self, email: str, password: str) -> Optional[Dict[str, Any]]:
        try:
            if not validate_email(email):
                print("Invalid email format. Please enter a valid email address.")
                return None

            if not validate_password(password):
                print("Password must be at least 3 characters long.")
                return None

            self.logger.info(f"Attempting login for email: {email}")
            response = self.api_client.post(
                "/auth/login", {"email": email, "password": password}
            )

            self.api_client.set_token(response["access_token"])
            self.logger.info(f"Login successful for email: {email}")

            profile = self.api_client.get("/users/me")
            print("Login successful.")
            print(f"Welcome, {profile['username']}!")

            return profile

        except AuthenticationError:
            print("Login failed. Please check your email and password.")
            return None
        except NetworkError as e:
            self.logger.error(f"Network error during login: {e}")
            print("Network error. Please check your connection and try again.")
            return None
        except DataProcessingError as e:
            self.logger.error(f"Data processing error during login: {e}")
            print("Login failed due to server error. Please try again later.")
            return None
        except Exception as e:
            self.logger.error(f"Unexpected error during login: {e}")
            print("An unexpected error occurred. Please try again.")
            return None

    def signup(
        self, username: str, email: str, password: str
    ) -> Optional[Dict[str, Any]]:
        try:
            if not validate_username(username):
                print(
                    "Username must be 3-20 characters long and contain only letters, numbers, and underscores."
                )
                return None

            if not validate_email(email):
                print("Invalid email format. Please enter a valid email address.")
                return None

            if not validate_password(password):
                print("Password must be at least 3 characters long.")
                return None

            self.logger.info(f"Attempting signup for email: {email}")
            response = self.api_client.post(
                "/auth/signup",
                {"username": username, "email": email, "password": password},
            )

            self.logger.info(f"Signup successful for email: {email}")
            print("Account created successfully!")
            print("Please login with your new credentials.")

            return None

        except AuthenticationError as e:
            self.logger.warning(f"Signup failed - authentication error: {e}")
            print("Signup failed. The email might already be registered.")
            return None
        except NetworkError as e:
            self.logger.error(f"Network error during signup: {e}")
            print("Network error. Please check your connection and try again.")
            return None
        except DataProcessingError as e:
            self.logger.error(f"Data processing error during signup: {e}")
            print("Signup failed due to server error. Please try again later.")
            return None
        except Exception as e:
            self.logger.error(f"Unexpected error during signup: {e}")
            print("An unexpected error occurred. Please try again.")
            return None


class LoginMenu(BaseMenu):
    pass

    def __init__(self, api_client: APIClient):
        self.auth_service = AuthenticationService(api_client)
        self.logger = logging.getLogger(__name__)

    def show(self) -> Optional[Dict[str, Any]]:
        self.print_header("Login / Signup")

        while True:
            try:
                choice = self._get_user_choice()

                if choice == "1":
                    user = self._handle_login()
                    if user:
                        return user
                elif choice == "2":
                    user = self._handle_signup()
                    if user:
                        return user
                elif choice == "0":
                    print("Goodbye!")
                    exit()
                else:
                    print("Invalid choice. Please select 1, 2, or 0.")

            except KeyboardInterrupt:
                print("\nGoodbye!")
                exit()
            except Exception as e:
                self.logger.error(f"Unexpected error in menu: {e}")
                print("An error occurred. Please try again.")

    def _get_user_choice(self) -> str:
        print("[1] Login")
        print("[2] Signup")
        print("[0] Exit")
        return input("Choice: ").strip()

    def _handle_login(self) -> Optional[Dict[str, Any]]:
        print("\n--- Login ---")
        email = input("Email: ").strip()
        password = input("Password: ").strip()

        if not email or not password:
            print("Email and password are required.")
            return None

        return self.auth_service.login(email, password)

    def _handle_signup(self) -> Optional[Dict[str, Any]]:
        print("\n--- Signup ---")
        username = input("Username: ").strip()
        email = input("Email: ").strip()
        password = input("Password: ").strip()

        if not username or not email or not password:
            print("Username, email, and password are required.")
            return None

        return self.auth_service.signup(username, email, password)
