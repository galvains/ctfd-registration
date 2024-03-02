import os
import re
import smtplib
import secrets
import requests
import string
import random

from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from jinja2 import Environment, FileSystemLoader

SENDER_EMAIL = os.getenv('SENDER_EMAIL')
SMTP_PORT = int(os.getenv('SMTP_PORT'))
SMTP_HOST = os.getenv('SMTP_HOST')
SENDER_PASSWORD = os.getenv('SENDER_PASSWORD')
CAPTCHA_URL = os.getenv('CAPTCHA_URL')
CAPTCHA_TOKEN = os.getenv('CAPTCHA_TOKEN')

alphabet = string.ascii_letters + string.digits


def generate_password():
    return ''.join(secrets.choice(alphabet) for _ in range(16))


def generate_username():
    gen = f"user_{''.join(random.choices(string.digits, k=6))}"
    return gen


def send_email(recipient: str, context: dict, selection: bool) -> None:
    message = MIMEMultipart()
    message["From"] = SENDER_EMAIL
    message["To"] = recipient
    if selection:
        message["Subject"] = "Регистрация Quizmine"
        message.attach(MIMEText(read_html_file('templates/email_registration.html', context), "html"))
    else:
        message["Subject"] = "Логин Quizmine"
        message.attach(MIMEText(read_html_file('templates/email_login.html', context), "html"))

    with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as server:
        server.starttls()
        server.login(SENDER_EMAIL, SENDER_PASSWORD)
        server.sendmail(SENDER_EMAIL, recipient, message.as_string())


def read_html_file(file_path: str, context: dict):
    env = Environment(loader=FileSystemLoader('.'))
    template = env.get_template(file_path)
    html_content = template.render(context)
    return html_content


def verify_hcaptcha(user_response):
    params = {
        'secret': CAPTCHA_TOKEN,
        'response': user_response,
    }
    response = requests.post(CAPTCHA_URL, data=params)
    result = response.json()
    return result["success"]


def valid_symbols(username: str) -> bool:
    return bool(re.match(r"^[\s\w.@+-]+\Z", username))
