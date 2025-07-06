

class MenuOptions:
 
    # Main menu options
    LOGIN = "1"
    SIGNUP = "2"
    EXIT = "0"

    # User menu options
    HEADLINES = "1"
    SAVED_ARTICLES = "2"
    SEARCH = "3"
    NOTIFICATIONS = "4"
    LOGOUT = "5"

    # Admin menu options
    VIEW_SERVER_STATUS = "1"
    VIEW_SERVER_DETAILS = "2"
    UPDATE_SERVER = "3"
    ADD_CATEGORY = "4"
    VIEW_REPORTED_ARTICLES = "5"
    HIDE_CATEGORY = "6"
    BLACKLIST_KEYWORD = "7"
    ADMIN_LOGOUT = "8"

    # Headlines sub-menu options
    TODAY = "1"
    DATE_RANGE = "2"
    BACK = "3"

    # Article interaction options
    BACK_OPTION = "1"
    SAVE_ARTICLE = "2"
    LIKE_ARTICLE = "3"
    DISLIKE_ARTICLE = "4"
    REPORT_ARTICLE = "5"

    # Notification menu options
    VIEW_NOTIFICATIONS = "1"
    CONFIGURE_NOTIFICATIONS = "2"
    NOTIFICATION_BACK = "3"
    NOTIFICATION_LOGOUT = "4"

    # Confirmation options
    YES = "y"
    NO = "n"
    YES_FULL = "yes"
    NO_FULL = "no"

    @classmethod
    def get_confirmation_options(cls) -> tuple:
        """Get all valid confirmation options."""
        return (cls.YES, cls.NO, cls.YES_FULL, cls.NO_FULL)

    @classmethod
    def is_confirmation_yes(cls, choice: str) -> bool:
        """Check if choice indicates yes."""
        return choice.lower() in (cls.YES, cls.YES_FULL)

    @classmethod
    def is_confirmation_no(cls, choice: str) -> bool:
        """Check if choice indicates no."""
        return choice.lower() in (cls.NO, cls.NO_FULL)
