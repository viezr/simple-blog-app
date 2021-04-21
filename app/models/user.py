"""
User model
"""

from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app import db, login


@login.user_loader
def user_loader(_id: int):
    """
    User loader
    """
    return User.query.get(int(_id))


class User(UserMixin, db.Model):
    """
    User model
    """
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), index=True, unique=True, nullable=False)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(256), nullable=False)
    image_file = db.Column(db.String(20), default="default.png", nullable=False )
    join_date = db.Column(db.DateTime, index=True, default=datetime.utcnow, nullable=False)
    posts = db.relationship("Post", backref="author", lazy=True)

    def __repr__(self):
        """
        Default representation method
        """
        return f"<User object (username: {self.username}, email:{self.email}, image:{self.image_file})>"

    def __str__(self):
        """
        Default string method
        """
        return f"User object (username: {self.username}, email:{self.email})"

    def set_password(self, pure_pass: str):
        """
        Set password attribute as hash generated from pure password
        """
        self.password_hash = generate_password_hash(pure_pass)

    def check_password(self, semi_pure_pass: str) -> bool:
        """
        Check conformity input password and stored hash
        """
        return check_password_hash(self.password_hash, semi_pure_pass)
