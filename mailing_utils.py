import os
import smtplib

from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from jinja2 import Environment, FileSystemLoader
from dotenv import load_dotenv

load_dotenv()

SENDER_EMAIL = os.getenv('SENDER_EMAIL')
SMTP_PORT = int(os.getenv('SMTP_PORT'))
SMTP_HOST = os.getenv('SMTP_HOST')
SENDER_PASSWORD = os.getenv('SENDER_PASSWORD')
CAPTCHA_URL = os.getenv('CAPTCHA_URL')
CAPTCHA_TOKEN = os.getenv('CAPTCHA_TOKEN')


def send_email(recipient: str, context: dict, selection: bool) -> None:
    message = MIMEMultipart()
    message["From"] = SENDER_EMAIL
    message["To"] = recipient
    if selection:
        message["Subject"] = "Регистрация Quizmine"
        message.attach(MIMEText(read_html_file('core/templates/email_registration.html', context), "html"))
    else:
        message["Subject"] = "Логин Quizmine"
        message.attach(MIMEText(read_html_file('core/templates/email_login.html', context), "html"))

    with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as server:
        server.starttls()
        server.login(SENDER_EMAIL, SENDER_PASSWORD)
        server.sendmail(SENDER_EMAIL, recipient, message.as_string())


def read_html_file(file_path: str, context: dict):
    env = Environment(loader=FileSystemLoader('.'))
    template = env.get_template(file_path)
    html_content = template.render(context)
    return html_content
