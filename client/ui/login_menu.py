from ui.base_menu import BaseMenu

class LoginMenu(BaseMenu):
    def __init__(self, api_client):
        self.api_client = api_client

    def show(self):
        self.print_header("Login / Signup")
        while True:
            choice = input("[1] Login\n[2] Signup\n[0] Exit\nChoice: ")
            if choice == "1":
                self.login()
                return
            elif choice == "2":
                self.signup()
            elif choice == "0":
                exit()
            else:
                print("Invalid choice.")

    def login(self):
        email = input("Email: ")
        password = input("Password: ")
        try:
            response = self.api_client.post("/auth/login", {"email": email, "password": password})
            self.api_client.set_token(response["access_token"])
            print("Login successful.")
        except Exception as e:
            print(f"Login failed: {e}")

    def signup(self):
        username = input("Username: ")
        email = input("Email: ")
        password = input("Password: ")
        try:
            response = self.api_client.post("/auth/signup", {"username": username, "email": email, "password": password})
            self.api_client.set_token(response["access_token"])
            print("Signup successful.")
        except Exception as e:
            print(f"Signup failed: {e}")
