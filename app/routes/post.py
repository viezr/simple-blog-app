"""
User route module
"""
from datetime import datetime
from flask import request, redirect, render_template, flash, url_for, abort
from flask_login import login_required, current_user
from app import app, db
from app.forms.posts import PostFormNew, PostFormEdit, PostFormDelete
from app.models.post import Post
from app.utils.compressor import save_picture


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
        if form.picture.data:
            picture_file = save_picture(form.picture.data, "post")
            post.image_file = picture_file
        current_user.posts.append(post)
        db.session.add(post)
        db.session.add(current_user)
        db.session.commit()
        flash("Congrats! Your post created successfully!", "success")
        return redirect(url_for("post_id", _id=post.id))

    return render_template("posts/posts_new.html",
                           user=current_user, form=form, title="New Post")


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
        if form.picture.data:
            picture_file = save_picture(form.picture.data, "post")
            post_db.image_file = picture_file
        post_db.title = form.title.data
        post_db.body = form.body.data
        post_db.time_updated = datetime.utcnow()
        db.session.add(post_db)
        db.session.commit()
        flash("Congrats! Your post successfully udated!", "success")
        return redirect(url_for("post_id", _id=post_db.id))

    form.title.data = post_db.title
    form.body.data = post_db.body

    image_file = None
    if post_db.image_file:
        image_file = url_for(
            'static',
            filename="img/posts/" +
            post_db.image_file)
    return render_template("posts/posts_edit.html", user=current_user,
                           image_file=image_file, form=form, title="Edit Post")


@app.route("/posts/<int:_id>", methods=["GET", "POST"])
@login_required
def post_id(_id=None):
    """
    Get post's infromation by ID
    """
    post_db = Post.query.get(_id)
    if post_db is None:
        flash("Post with that ID not found", "danger")
        return redirect(url_for("posts"))

    post_db.views_counter += 1
    db.session.add(post_db)
    db.session.commit()

    if request.method == "POST" and post_db.author != current_user:
        abort(403)
    form = PostFormDelete()
    if request.method == "POST" and form.validate():
        db.session.delete(post_db)
        db.session.commit()
        flash("Your post has been deleted!", "success")
        return redirect(url_for("posts"))

    return render_template("posts/posts_id.html", form=form,
                           user=current_user, post=post_db, title="Post info")
