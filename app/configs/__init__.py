"""
Inintial config
"""
import os


class Config():
    """
    Config attributes
    """

    SECRET_KEY = os.environ.get("SECRET_KEY") or "LKJF887393UFOIJDKJjkjdf"
    SQLALCHEMY_DATABASE_URI = os.environ.get("DB_URI")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    MAIL_PORT = 465
    MAIL_SERVER = "smtp.mail.ru"
    MAIL_USE_SSL = True
    MAIL_USERNAME = os.environ.get("EMAIL_ADMIN")
    MAIL_PASSWORD = os.environ.get("EMAIL_ADMIN_PASSWORD")
