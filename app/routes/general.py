"""
General route
"""
from flask import render_template, request
from flask_login import current_user
from app import app, db
from app.models.post import Post


@app.route("/", methods=["GET"])
@app.route("/homepage", methods=["GET"])
def homepage():
    """
    Home page render
    """
    posts_db = Post.query.order_by(Post.time_updated.desc())[:-4:]
    return render_template("index.html", posts=posts_db,
                           user=current_user, title="Home Page")


@app.route("/posts", methods=["GET"])
def posts():
    """
    Posts page render
    """
    page = request.args.get("page", 1, type=int)
    posts_db = Post.query.order_by(
        Post.time_updated.desc()).paginate(
        page=page, per_page=6)
    return render_template("posts/posts.html", posts=posts_db,
                           user=current_user, title="Blogs Page")


@app.route("/about", methods=["GET"])
def about():
    """
    About page render
    """
    return render_template("about.html", user=current_user, title="Blogs Page")
