from sqlalchemy.orm import Session
from app.utils.email_utils import send_email
from typing import Optional
from app.exceptions.custom_exceptions import EmailException, UserException


class EmailService:
    def __init__(self, db):
        self.db = db

    def send_notification_email(
        self, user_id: int, message: str, url: Optional[str] = None
    ):
        try:
            from app.models.user import User

            user = self.db.query(User).filter_by(id=user_id).first()
            if not user:
                raise UserException(
                    f"User with ID {user_id} not found", user_id=user_id
                )

            subject = "📰 New Notification - News Aggregator"

            html_message = f"""
            <html>
                <body>
                    <p>Hi <strong>{user.email}</strong>,</p>
                    <p>{message}</p>
            """

            if url:
                html_message += f'<p><a href="{url}">🔗 Read Full Article</a></p>'

            html_message += """
                    <br><p>🗞️ Stay informed,<br>News Aggregator Team</p>
                </body>
            </html>
            """

            send_email(user.email, subject, html_message, html_format=True)
        except UserException:
            raise
        except Exception as e:
            recipient_email = user.email if "user" in locals() and user else None
            raise EmailException(
                f"Failed to send notification email: {str(e)}",
                recipient=recipient_email,
                subject="Notification",
            )
