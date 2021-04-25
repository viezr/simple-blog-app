"""
User route module
"""
from flask import request, redirect, render_template, flash, url_for
from flask_login import logout_user, current_user, login_user, login_required
from app import app, db
from app.forms.user import RegisterForm, LoginForm, UpdateForm, PasswordForm, RequestTokenForm, PasswordResetForm, ReportForm
from app.models.user import User
from app.models.post import Post
from app.routes.general import homepage
from app.utils.compressor import save_picture
from app.utils.email import send_reset_email, send_report_email, send_confirmation_email


@app.route("/user/<string:username>", methods=["GET"])
def user_public(username: str):
    """
    Public user profile
    """
    user = User.query.filter_by(username=username).first_or_404()
    page = request.args.get("page", 1, type=int)
    posts_db = Post.query.filter_by(
        author=user).order_by(
        Post.time_updated.desc()).paginate(page=page, per_page=6)

    return render_template("users/user_public.html", posts=posts_db,
                           user=user, title=f"{user.username}'s profile")


@app.route("/reset_password/", methods=["GET", "POST"])
def reset_password_token():
    """
    Request reset password
    """
    if current_user.is_authenticated:
        flash("User already logged in!", "success")
        return redirect(url_for('homepage'))

    form = RequestTokenForm()
    if request.method == "POST" and form.validate():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash("An email has been sent with instructions for reset password", "info")
        return redirect(url_for("login"))

    return render_template("users/user_request_token.html",
                           title="Reset password form",
                           legend="Reset Password",
                           submit_button="Reset password",
                           form=form)


@app.route("/reset_password/<token>", methods=["GET", "POST"])
def reset_password(token):
    """
    Reset password with token
    """
    if current_user.is_authenticated:
        flash("User already logged in!", "success")
        return redirect(url_for('homepage'))

    user = User.verify_token(token)
    if user is None:
        flash("This is an invalid or expired token", "warning")
        return redirect(url_for("reset_password"))

    form = PasswordResetForm()
    if request.method == "POST" and form.validate():
        user.set_password(form.new_password_1.data)
        db.session.commit()

        flash("Password successfully changed", "success")
        return redirect(url_for("login"))

    return render_template("users/user_password_reset.html",
                           title="Reset password", form=form)


@app.route("/confirmation", methods=["GET", "POST"])
def confirmation():
    """
    Account confirmation request
    """
    form = RequestTokenForm()
    if request.method == "POST" and form.validate():
        user = User.query.filter_by(email=form.email.data).first()
        send_confirmation_email(user)
        flash(
            "An email has been sent with instructions for account confirmation",
            "info")
        return redirect(url_for("homepage"))

    return render_template("users/user_request_token.html",
                           title="Email confirmation",
                           legend="Confirm your email address",
                           submit_button="Send confirmation link",
                           form=form)


@app.route("/confirmation/<token>", methods=["GET", "POST"])
def confirmation_set(token):
    """
    Set account confirmation status
    """
    if current_user.is_authenticated:
        flash("User already logged in!", "success")
        return redirect(url_for('homepage'))
    user = User.verify_token(token)
    if user is None:
        flash("This is an invalid or expired token", "warning")
        return redirect(url_for("confirmation"))

    user.confirmed = True
    db.session.commit()

    flash(
        "Congrats! Your account was successfully confirmed! Now you can log in!",
        "success")
    return redirect(url_for("login"))


@app.route("/login", methods=["GET", "POST"])
def login():
    """
    Login route
    """

    if current_user.is_authenticated:
        flash("User already logged in!", "success")
        return redirect(url_for('homepage'))
    form = LoginForm()
    if request.method == "POST" and form.validate():
        user = User.query.filter_by(email=form.email.data).first()
        if user is None or not user.check_password(form.password.data):
            flash("Invalid email or password", "danger")
            return redirect(url_for("login"))
        if not user.confirmed:
            flash("To log in you have to confirm your account", "warning")
            return redirect(url_for("confirmation"))

        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get("next")
        return redirect(next_page) if next_page else redirect(
            url_for("homepage"))
    return render_template("users/user_login.html", title="Log In", form=form)


@app.route("/register", methods=["GET", "POST"])
def register():
    """
    Register route
    """
    if current_user.is_authenticated:
        flash("User already logged in!", "success")
        return redirect(url_for("homepage"))

    form = RegisterForm()
    if request.method == "POST" and form.validate():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash("Congrats! Your account created successfully!", "success")
        return redirect(url_for("login"))

    return render_template("users/user_register.html",
                           form=form, title="Register")


@app.route("/password", methods=["GET", "POST"])
@login_required
def change_password():
    """
    Edit route
    """
    if not current_user.is_authenticated:
        return redirect(url_for('login'))

    user = current_user
    form = PasswordForm()
    form.current_user(user)

    if request.method == "POST" and form.validate():
        user.set_password(form.new_password_1.data)
        db.session.add(user)
        db.session.commit()
        flash("You password has been updated", "success")
        return redirect(url_for("homepage"))

    return render_template("users/user_password.html",
                           user=current_user, form=form, title="Change password")


@app.route("/profile", methods=["GET", "POST"])
@login_required
def profile():
    """
    Profile page render
    """
    form = UpdateForm()

    if request.method == "POST" and form.validate():
        if form.picture.data:
            picture_file = save_picture(form.picture.data, "user")
            current_user.image_file = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash("Your account info updated!", "success")
        return redirect(url_for("profile"))

    form.username.data = current_user.username
    form.email.data = current_user.email

    image_file = url_for(
        'static',
        filename="img/profiles/" +
        current_user.image_file)
    return render_template("users/user_profile.html", title="Profile",
                           user=current_user, image_file=image_file, form=form)


@app.route("/report", methods=["GET", "POST"])
@login_required
def report():
    """
    Report route
    """
    form = ReportForm()
    if request.method == "POST" and form.validate():
        send_report_email(current_user, form.subject.data, form.report.data)
        flash("An report email has been sent", "info")
        return redirect(url_for("homepage"))

    return render_template("users/user_report.html", title="Report", form=form)


@app.route("/logout", methods=["GET"])
@login_required
def logout():
    """
    Log out route
    """
    flash("User successfully logged out", "success")
    logout_user()
    return redirect(url_for("homepage"))
