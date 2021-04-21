"""
User route module
"""
from datetime import datetime
from flask import request, redirect, render_template, flash, url_for, abort
from flask_login import login_required, current_user
from app import app, db
from app.forms.posts import PostFormNew, PostFormEdit, PostFormDelete
#from app.models.user import User
from app.models.post import Post


@app.route("/posts/new", methods=["GET", "POST"])
@login_required
def post_new():
    """
    New post route
    """
    form = PostFormNew()
    if request.method == "POST" and form.validate():
        post = Post(
            title=form.title.data,
            body=form.body.data)
        current_user.posts.append(post)
        db.session.add(post)
        db.session.add(current_user)
        db.session.commit()
        flash("Congrats! Your post created successfully!", "success")
        return redirect(url_for("post", id=post.id))

    return render_template("posts_new.html", user=current_user, form=form, title="New Post")


@app.route("/posts/<int:_id>", methods=["GET"])
@login_required
def post_id(_id=None):
    """
    Get post's infromation by ID
    """
    post_db = Post.query.get(_id)
    if post_db is None:
        flash("Post with that ID not found", "danger")
        return redirect(url_for("posts"))
    return render_template("posts_id.html", user=current_user, post=post_db, title="Post info")


@app.route("/posts/<int:_id>/edit", methods=["GET", "POST"])
@login_required
def post_edit(_id=None):
    """
    Edit post route
    """
    post_db = Post.query.get(_id)
    if post_db.author != current_user:
        abort(403)

    form = PostFormEdit()
    if request.method == "POST" and form.validate():
        post_db.title = form.title.data
        post_db.body = form.body.data
        post_db.time_updated = datetime.utcnow()
        db.session.add(post_db)
        db.session.commit()
        flash("Congrats! Your post successfully udated!", "success")
        return redirect(url_for("post", _id=post.id))
    else:
        form.title.data = post_db.title
        form.body.data = post_db.body
    return render_template("posts_edit.html", user=current_user, form=form, title="Edit Post")


@app.route("/posts/<int:_id>/delete", methods=["GET", "POST"])
@login_required
def post_delete(_id=None):
    """
    Edit post route
    """
    form = PostFormDelete()
    post_db = Post.query.get(_id)
    if request.method == "POST" and form.validate():
        db.session.delete(post_db)
        db.session.commit()
        flash("Congrats! Your post deleted!", "success")
        return redirect(url_for("posts"))
    return render_template("posts_delete.html", user=current_user, form=form, title="Delete Post")
