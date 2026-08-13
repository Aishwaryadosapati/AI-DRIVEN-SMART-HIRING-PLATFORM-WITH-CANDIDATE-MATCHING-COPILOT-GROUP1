import smtplib
from email.mime.text import MIMEText
import os

from dotenv import load_dotenv

load_dotenv()

SENDER_EMAIL = os.getenv("SENDER_EMAIL")
APP_PASSWORD = os.getenv("APP_PASSWORD")


def send_email(receiver_email, subject, body):

    msg = MIMEText(body)

    msg["Subject"] = subject
    msg["From"] = SENDER_EMAIL
    msg["To"] = receiver_email

    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()

    server.login(
        SENDER_EMAIL,
        APP_PASSWORD
    )

    server.send_message(msg)

    server.quit()