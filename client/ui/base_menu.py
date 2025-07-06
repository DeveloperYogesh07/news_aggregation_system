import logging
from typing import Optional


class BaseMenu:

    def __init__(self):
        self.logger = logging.getLogger(self.__class__.__name__)

    def print_header(self, title: str) -> None:
        print("\n" + "=" * 50)
        print(title.center(50))
        print("=" * 50)

    def print_separator(self, length: int = 40) -> None:
        print("-" * length)

    def pause(self, message: str = "Press Enter to continue...") -> None:
        input(f"\n{message}")

    def get_user_input(self, prompt: str, required: bool = True) -> Optional[str]:
        while True:
            try:
                user_input = input(prompt).strip()
                if not user_input and required:
                    print("This field is required. Please try again.")
                    continue
                return user_input if user_input else None
            except KeyboardInterrupt:
                print("\nInput cancelled.")
                return None
            except Exception as e:
                self.logger.error(f"Error getting user input: {e}")
                print("An error occurred. Please try again.")

    def confirm_action(self, message: str = "Are you sure? (y/n): ") -> bool:
        while True:
            try:
                response = input(message).strip().lower()
                if response in ("y", "yes"):
                    return True
                elif response in ("n", "no"):
                    return False
                else:
                    print("Please enter 'y' or 'n'.")
            except KeyboardInterrupt:
                print("\nAction cancelled.")
                return False
            except Exception as e:
                self.logger.error(f"Error getting confirmation: {e}")
                print("An error occurred. Please try again.")

    def display_error(self, message: str) -> None:
        print(f"\n❌ Error: {message}")
        self.logger.error(message)

    def display_success(self, message: str) -> None:
        print(f"\n✅ {message}")
        self.logger.info(message)

    def display_info(self, message: str) -> None:
        print(f"\nℹ️  {message}")
        self.logger.info(message)
