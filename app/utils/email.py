"""
Module for sending email with token for reset password
"""
from flask import url_for
from flask_mail import Message
from app import mail, app


def send_reset_email(user):
    """
    Send email with token for reset password
    """
    token = user.get_reset_token()
    msg = Message(
        "Password reset request",
        sender=app.config["MAIL_USERNAME"],
        recipients=[user.email])
    msg.body = f"""
    To reset your password visit following link:

    {url_for("reset_password", token=token, _external=True)}

    Best Regards!
    """

    mail.send(msg)
