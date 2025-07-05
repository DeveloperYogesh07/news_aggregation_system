import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from app.core.config import settings as config


def send_email(to: str, subject: str, body: str, html_format: bool = False):
    smtp_server = config.SMTP_SERVER
    smtp_port = config.SMTP_PORT
    smtp_user = config.SMTP_USER
    smtp_password = config.SMTP_PASSWORD  

    try:
        msg = MIMEMultipart()
        msg["From"] = smtp_user
        msg["To"] = to
        msg["Subject"] = subject

        msg_type = "html" if html_format else "plain"
        msg.attach(MIMEText(body, msg_type))

        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(smtp_user, smtp_password)
            server.sendmail(smtp_user, to, msg.as_string())

        print(f"Email sent to {to}")
    except Exception as e:
        print(f"Failed to send email to {to}: {e}")
