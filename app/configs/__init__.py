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
