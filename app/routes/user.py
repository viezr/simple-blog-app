"""
User route module
"""
from flask import request, redirect, render_template, flash, url_for
from flask_login import logout_user, current_user, login_user, login_required
from app import app, db
from app.forms.user import RegisterForm, LoginForm, UpdateForm, PasswordForm
from app.models.user import User
from app.routes.general import homepage
from app.utils.compressor import save_picture

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
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get("next")
        return redirect(next_page) if next_page else url_for("homepage")
    return render_template("user_login.html", title="Log In", form=form)


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

    return render_template("user_register.html", form=form, title="Register")


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

    return render_template("user_password.html", user=current_user, form=form, title="Change password")


@app.route("/profile", methods=["GET", "POST"])
@login_required
def profile():
    """
    Profile page render
    """
    form = UpdateForm()

    if request.method == "POST" and form.validate():
        print(form.picture.data)
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash("Your account info updated!", "success")
        return redirect(url_for("profile"))
    else:
        form.username.data = current_user.username
        form.email.data = current_user.email

    image_file = url_for('static', filename="img/profiles/" + current_user.image_file)
    return render_template("user_profile.html", title="Profile", user=current_user, image_file=image_file, form=form)

@app.route("/logout", methods=["GET"])
@login_required
def logout():
    """
    Log out route
    """
    flash("User successfully logged out", "success")
    logout_user()
    return redirect(url_for("homepage"))
