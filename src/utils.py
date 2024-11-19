import re
import smtplib
import secrets

import requests
import string
import random

from passlib.hash import bcrypt_sha256
# from celery import Celery

from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from jinja2 import Environment, FileSystemLoader

from src.config import captcha, mail

SENDER_EMAIL = mail.email
SMTP_PORT = mail.port
SMTP_HOST = mail.host
SENDER_PASSWORD = mail.pwd
CAPTCHA_URL = captcha.url
CAPTCHA_TOKEN = captcha.token

alphabet = string.ascii_letters + string.digits


# celery = Celery('mailer')


def generate_username() -> str:
    return f"user_{''.join(secrets.choice(alphabet) for _ in range(4))}{''.join(random.choices(string.digits, k=6))}"


# @celery.task
def send_email(recipient: str, context: dict) -> None:
    message = MIMEMultipart()
    message["From"] = SENDER_EMAIL
    message["To"] = recipient
    message["Subject"] = "Регистрация на Событие"
    message.attach(MIMEText(read_html_file('src/templates/emails/email_template.html', context), "html"))

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


def hash_password(pwd: str) -> str:
    return bcrypt_sha256.hash(pwd)


def verify_password(plain_pwd: str, hash_pwd: str) -> bool:
    return bcrypt_sha256.verify(plain_pwd, hash_pwd)


def valid_symbols(username: str) -> bool:
    return bool(re.match(r"^[\s\w.@+-]+\Z", username))


def valid_telegram_tag(tag: str) -> bool:
    return bool(re.match(r'^@[a-zA-Z0-9_]{5,}$', tag))


def valid_age(age: str) -> bool:
    return bool(re.match(r'^(120|1[01][0-9]|[1-9]?[0-9])$', age))
