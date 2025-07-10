import logging
from typing import Optional, Dict, Any
from services.api_client import APIClient
from exceptions.custom_exceptions import (
    AuthenticationError,
    NetworkError,
    DataProcessingError,
    ClientError,
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

            try:
                profile = self.api_client.get("/users/me")
                print("Login successful.")
                print(f"Welcome, {profile['username']}!")
                return profile
            except Exception as profile_error:
                self.logger.warning(
                    f"Failed to fetch profile but login was successful: {profile_error}"
                )
                print("Login successful.")
                print("Welcome!")
                # Return a basic profile with email since we have the token
                return {"email": email, "username": email.split("@")[0]}

        except AuthenticationError as e:
            self.logger.warning(f"Authentication failed: {e} (type: {type(e).__name__})")
            print("Invalid email or password. Please try again.")
            return None
        except NetworkError as e:
            self.logger.warning(f"Network error: {e} (type: {type(e).__name__})")
            print("Connection error. Please check your internet connection.")
            return None
        except DataProcessingError as e:
            self.logger.error(f"Data processing error: {e} (type: {type(e).__name__})")
            print("Server error. Please try again later.")
            return None
        except ClientError as e:
            self.logger.error(f"Client error during login: {e} (type: {type(e).__name__})")
            print("An error occurred. Please try again.")
            return None
        except Exception as e:
            self.logger.error(f"Unexpected error during login: {e} (type: {type(e).__name__})")
            print("An error occurred. Please try again.")
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

        except AuthenticationError:
            print("Email already registered. Please use a different email.")
            return None
        except NetworkError:
            print("Connection error. Please check your internet connection.")
            return None
        except DataProcessingError:
            print("Server error. Please try again later.")
            return None
        except Exception as e:
            self.logger.error(f"Unexpected error during signup: {e}")
            print("An error occurred. Please try again.")
            return None
