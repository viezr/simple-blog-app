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
    token = user.get_token()

    msg = Message(
        "Password reset request",
        sender=app.config["MAIL_USERNAME"],
        recipients=[user.email])
    msg.body = f"""
    To reset your password visit following link:

    {url_for("reset_password", token=token, _external=True)}

    Best Regards!
    """

    if app.config["MAIL_SUPPRESS_SEND"] == "True":
        print(f"""Mail supress mode is ON. Sending email to { user.email }.
            Token: { token }""")
    else:
        mail.send(msg)


def send_confirmation_email(user):
    """
    Send email with token for reset password
    """
    token = user.get_token()

    msg = Message(
        "Account confirmation",
        sender=app.config["MAIL_USERNAME"],
        recipients=[user.email])
    msg.body = f"""
    To confirm your account visit following link:

    {url_for("confirmation_set", token=token, _external=True)}

    Best Regards!
    """

    if app.config["MAIL_SUPPRESS_SEND"] == "True":
        print(f"""Mail supress mode is ON. Sending email to { user.email }.
            Token: { token }""")
    else:
        mail.send(msg)


def send_report_email(user, subject, report):
    """
    Send report email
    """
    msg = Message(
        "Report from " + user.username,
        sender=user.email,
        recipients=[app.config["MAIL_USERNAME"]])
    msg.body = f"""
    Report from user: {user.username}, mail: {user.email}
    Report title: {subject}
    Report text:
    ====================================================
    {report}
    ====================================================
    """

    msg_user = Message(
        "Password reset request",
        sender=app.config["MAIL_USERNAME"],
        recipients=[user.email])
    msg_user.body = f"""
    Hello {user.username}!
    We've recieved your report, and soon will answer to you.

    Best Regards!
    """

    if app.config["MAIL_SUPPRESS_SEND"] == "True":
        print(f"""
            Mail supress mode is ON.
            Sending email to { app.config["MAIL_USERNAME"] } from { user.email }. Body:
            { msg.body }
            """)

        print(f"""
            Sending email to { user.email } from { app.config["MAIL_USERNAME"] }. Body:
            { msg_user.body }
            """)
    else:
        mail.send(msg)
        mail.send(msg_user)
