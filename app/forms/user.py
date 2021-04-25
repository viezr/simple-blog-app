"""
User module for web-forms
"""
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, BooleanField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, EqualTo, Email, ValidationError, Length
from flask_login import current_user
from flask_babel import lazy_gettext as _l
from app.models.user import User


class LoginForm(FlaskForm):
    """
    Form class for user login
    """
    email = StringField(
        label=_l("Email"),
        validators=[
            DataRequired(),
            Email()])
    password = PasswordField(label=_l("Password"), validators=[DataRequired()])
    remember_me = BooleanField(label=_l("Remember?"))
    submit = SubmitField(label=_l("Log In Button"))


class ReportForm(FlaskForm):
    """
    Form class for report
    """
    subject = StringField(label=_l("Subject"), validators=[DataRequired()])
    report = TextAreaField(label=_l("Text"), validators=[DataRequired()])
    submit = SubmitField(label=_l("Send Report"))


class RegisterForm(FlaskForm):
    """
    Form class for register new user
    """
    username = StringField(
        label="Username", validators=[
            DataRequired(), Length(
                3, 64)])
    email = StringField(label="Email", validators=[DataRequired(), Email()])
    password = PasswordField(label="Password", validators=[DataRequired()])
    password2 = PasswordField(
        label="Password(Again)", validators=[
            DataRequired(), EqualTo("password")])
    submit = SubmitField(label="Register Button")

    def validate_username(self, field):
        """
        Is user with given username in database
        """
        user = User.query.filter_by(username=field.data).first()
        if user:
            raise ValidationError("Please use different name")

    def validate_email(self, field):
        """
        Is user with given email in database
        """
        user = User.query.filter_by(email=field.data).first()
        if user:
            raise ValidationError("Please use different email")


class UpdateForm(FlaskForm):
    """
    Form for update user details
    """
    username = StringField(
        label="Username", validators=[
            DataRequired(), Length(
                3, 64)])
    email = StringField(label="Email")
    picture = FileField(label="Update Profile Picture", validators=[
                        FileAllowed(["png", "jpg", "jpeg"])])
    submit = SubmitField(label="Update")

    def validate_username(self, field):
        """
        Is user with given username in database
        """
        if field.data != current_user.username:
            user = User.query.filter_by(username=field.data).first()
            if user:
                raise ValidationError("Please use different name")

    def validate_email(self, field):
        """
        Is user with given email in database
        """
        if field.data != current_user.email:
            user = User.query.filter_by(email=field.data).first()
            if user:
                raise ValidationError("Please use different email")


class PasswordForm(FlaskForm):
    """
    Form class for changing user password
    """

    def current_user(self, user):
        """
        Get user object
        """
        self.user = user

    old_password = PasswordField(label="Old password")
    new_password_1 = PasswordField(label="New password")
    new_password_2 = PasswordField(label="New password (Again)")
    submit = SubmitField(label="Update my password")

    def validate_old_password(self, field):
        """
        Check old password isn't empty and correct
        """
        if field.data is None or field.data == "":
            raise ValidationError("This field can not be blank!")
        if not self.user.check_password(field.data):
            raise ValidationError("Invalid credentials for old password")

    def validate_new_password_1(self, field):
        """
        Check new password 1 isn't empty, equal to new password 2 and doesn't match old password
        """
        if field.data is None or field.data == "":
            raise ValidationError("This field can not be blank!")
        if not field.data == self.new_password_2.data:
            raise ValidationError("New passwords should match!")
        if self.user.check_password(field.data):
            raise ValidationError(
                "New password should not match with old password")

    def validate_new_password_2(self, field):
        """
        Check new password 2 isn't empty and doesn't match old password
        """
        if field.data is None or field.data == "":
            raise ValidationError("This field can not be blank!")
        if self.user.check_password(field.data):
            raise ValidationError(
                "New password should not match with old password")


class RequestTokenForm(FlaskForm):
    """
    Form class request token for confirmation email or changing user password
    """
    email = StringField(label="Email", validators=[DataRequired(), Email()])
    submit = SubmitField(label="Reset Password")

    def validate_email(self, field):
        """
        Is user with given email in database
        """
        user = User.query.filter_by(email=field.data).first()
        if user is None:
            raise ValidationError("There are no accounts with that email.")


class PasswordResetForm(FlaskForm):
    """
    Form class for changing user password
    """
    new_password_1 = PasswordField(
        label="New password", validators=[
            DataRequired()])
    new_password_2 = PasswordField(
        label="New password (Again)", validators=[
            DataRequired(), EqualTo("new_password_1")])
    submit = SubmitField(label="Set new password")
