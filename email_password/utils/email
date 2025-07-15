import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from dotenv import load_dotenv

load_dotenv()

SMTP_USER = os.getenv("SMTP_USER")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD")
FRONTEND_RESET_URL = os.getenv("FRONTEND_RESET_URL")


def send_reset_email(to_email: str, reset_token: str):
    msg = MIMEMultipart()
    msg["Subject"] = "Réinitialisation de votre mot de passe"
    msg["From"] = SMTP_USER
    msg["To"] = to_email

    reset_url = f"{FRONTEND_RESET_URL}?token={reset_token}"
    body = f"Voici votre lien pour réinitialiser votre mot de passe :\n{reset_url}\n\nLe lien expire dans 30 minutes."

    msg.attach(MIMEText(body, "plain"))

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(SMTP_USER, SMTP_PASSWORD)
        server.send_message(msg)
