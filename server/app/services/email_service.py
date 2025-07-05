from pytest import Session
from app.utils.email_utils import send_email


class EmailService:
    def __init__(self, db):
        self.db = db

    def send_notification_email(self, user_id: int, message: str, url: str = None):
        from app.models.user import User
        user = self.db.query(User).filter_by(id=user_id).first()
        if not user:
            return

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

