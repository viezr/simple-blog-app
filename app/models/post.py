"""
Post model
"""

from datetime import datetime
from app import db


class Post(db.Model):
    """
    Post model
    """
    __tablename__ = "posts"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(128), index=True, nullable=False)
    body = db.Column(db.Text, nullable=False)
    time_created = db.Column(
        db.DateTime,
        index=True,
        default=datetime.utcnow,
        nullable=False)
    time_updated = db.Column(
        db.DateTime,
        index=True,
        default=datetime.utcnow,
        nullable=False)
    image_file = db.Column(db.String(20))
    views_counter = db.Column(db.Integer, nullable=False, default=0)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)

    def __str__(self):
        """
        Default str method
        """
        return f"Post object (title: {self.title}, body: {self.body}, author: {self.time_created})"

    def __repr__(self):
        """
        Default representation method
        """
        return f"<Post object (title: {self.title}, body: {self.body}, author: {self.time_created})>"
