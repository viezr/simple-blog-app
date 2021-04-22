"""
General route
"""
from flask import render_template, request
from flask_login import login_required, current_user
from app import app, db
from app.models.post import Post


@app.route("/", methods=["GET"])
@app.route("/homepage", methods=["GET"])
def homepage():
    """
    Home page render
    """
    page = request.args.get("page", 1, type=int)
    posts_db = Post.query.order_by(Post.time_updated).paginate(page=page,per_page=2)
    # posts.items

#    posts_db = Post.query.order_by(Post.time_updated).all()[:-4:-1]
    return render_template("index.html", posts=posts_db, user=current_user, title="Home Page")

@app.route("/posts", methods=["GET"])
def posts():
    """
    Posts page render
    """

    posts_db = Post.query.order_by(Post.time_updated).all()[::-1]
    return render_template("posts.html", posts=posts_db, user=current_user, title="Blogs Page")

@app.route("/about", methods=["GET"])
def about():
    """
    About page render
    """
    return render_template("about.html", user=current_user, title="Blogs Page")
