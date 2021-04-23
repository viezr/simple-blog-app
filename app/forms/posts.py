"""
User module for web-forms
"""
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired


class PostForm():
    """
    Core attributes for post forms
    """
    title = StringField(label="Post Title", validators=[DataRequired()])
    body = TextAreaField(label="Post body", validators=[DataRequired()])
    picture = FileField(label="Add post picture", validators=[
                        FileAllowed(["png", "jpg", "jpeg"])])


class PostFormNew(FlaskForm, PostForm):
    """
    Form class for new post
    """
    submit = SubmitField(label="Post it!")


class PostFormEdit(FlaskForm, PostForm):
    """
    Form class for edit post
    """
    submit = SubmitField(label="Update this Post")


class PostFormDelete(FlaskForm):
    """
    Form class for delete post
    """
    submit = SubmitField(label="Delete Post")
