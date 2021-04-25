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

    MAIL_SERVER = "smtp.office365.com"
    MAIL_USE_SSL = True
    MAIL_PORT = 465
    MAIL_USERNAME = os.environ.get("EMAIL_ADMIN")
    MAIL_PASSWORD = os.environ.get("EMAIL_ADMIN_PASSWORD")
    MAIL_SUPPRESS_SEND = True

    LANGUAGES = ["en", "ru"]
