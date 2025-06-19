from services.api_client import APIClient
from ui.login_menu import LoginMenu
from ui.user_menu import UserMenu
from ui.admin_menu import AdminMenu

def main():
    api_client = APIClient()
    login_menu = LoginMenu(api_client)

    while True:
        login_menu.show()
        try:
            user = api_client.get("/users/me")  
            if user.get("is_admin"):
                AdminMenu(api_client).show()
            else:
                UserMenu(api_client).show()
        except Exception as e:
            print(f"Error fetching user profile: {e}")

if __name__ == "__main__":
    main()
