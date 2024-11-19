import os

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    SECRET_KEY: str
    CAPTCHA_URL: str
    CAPTCHA_TOKEN: str
    SMTP_EMAIL: str
    SMTP_PASSWORD: str
    SMTP_HOST: str
    SMTP_PORT: str
    MAX_TEAM_SIZE: int
    MYSQL_HOST: str
    MYSQL_ROOT_PASSWORD: str
    MYSQL_USER: str
    MYSQL_PASSWORD: str
    MYSQL_DATABASE: str

    model_config = SettingsConfigDict(env_file=os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".env"))


settings = Settings()


class Captcha:
    def __init__(self, captcha_url, captcha_token):
        self.url = captcha_url
        self.token = captcha_token


class Mail:
    def __init__(self, smtp_email, smtp_pwd, smtp_host, smtp_port):
        self.email = smtp_email
        self.pwd = smtp_pwd
        self.host = smtp_host
        self.port = smtp_port


captcha = Captcha(
    captcha_url=settings.CAPTCHA_URL,
    captcha_token=settings.CAPTCHA_TOKEN
)

mail = Mail(
    smtp_email=settings.SMTP_EMAIL,
    smtp_pwd=settings.SMTP_PASSWORD,
    smtp_host=settings.SMTP_HOST,
    smtp_port=settings.SMTP_PORT
)


def get_database_url() -> str:
    return f"mysql+pymysql://{settings.MYSQL_USER}:{settings.MYSQL_PASSWORD}@{settings.MYSQL_HOST}/{settings.MYSQL_DATABASE}?charset=utf8mb4"


def get_secret_key() -> str:
    return settings.SECRET_KEY


def get_team_size() -> int:
    return settings.MAX_TEAM_SIZE
