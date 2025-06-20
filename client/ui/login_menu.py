from ui.base_menu import BaseMenu

class LoginMenu(BaseMenu):
    def __init__(self, api_client):
        self.api_client = api_client

    def show(self):
        self.print_header("Login / Signup")

        while True:
            choice = input("[1] Login\n[2] Signup\n[0] Exit\nChoice: ")

            if choice == "1":
                user = self.login()
                if user:
                    return user  
            elif choice == "2":
                self.signup()
            elif choice == "0":
                print("Goodbye!")
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

            profile = self.api_client.get("/users/me")
            print(f"Welcome, {profile['username']}!")
            return profile
        except Exception as e:
            print(f"Login failed. Please check your email or password and try again")
            return None

    def signup(self):
        username = input("Username: ")
        email = input("Email: ")
        password = input("Password: ")
        try:
            response = self.api_client.post("/auth/signup", {"username": username, "email": email, "password": password})
            self.api_client.set_token(response["access_token"])
            print("Signup successful.")

            profile = self.api_client.get("/users/me")
            print(f"Welcome, {profile['username']}!")
            return profile
        except Exception as e:
            print(f"Signup failed: {e}")
            return None
