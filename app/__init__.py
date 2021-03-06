"""
App's Core
"""
from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_mail import Mail
from app.configs import Config
from flask_babel import Babel

app = Flask(__name__)
app.config.from_object(Config)

db = SQLAlchemy(app)
migrate = Migrate(app, db)

login = LoginManager(app)
login.login_view = "login"
login.login_message_category = "info"

mail = Mail(app)
babel = Babel(app)

@babel.localeselector
def get_locale():
    return request.accept_languages.best_match(app.config["LANGUAGES"])

from app.models.user import User
from app.models.post import Post
from app.routes.general import *
from app.routes.user import *
from app.routes.post import *
from app.errors.handlers import *

from app.api import *
