from ui.login_menu import LoginMenu
from ui.admin_menu import AdminMenu
from ui.user_menu import UserMenu
from services.api_client import APIClient

def main():
    api_client = APIClient()

    while True:
        login_menu = LoginMenu(api_client)
        user = login_menu.show()  

        if not user:
            continue  

        if user["is_admin"]:
            AdminMenu(api_client).show()
        else:
            UserMenu(api_client).show()

if __name__ == "__main__":
    main()
