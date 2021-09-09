"""
REST API addition for JSON input-output
"""
from flask import jsonify
from app import app
from app.models.post import Post


@app.route("/api/v1/posts", methods=["GET"])
def get_post_api():
    """
    API function for get all posts
    """
    pass


@app.route("/api/v1/posts/<int:_id>", methods=["GET"])
def get_posts_api(_id: int):
    """
    API function for get posts by ID
    """
    post = Post.query.get(_id)
    if post is None:
        return jsonify({"Message": "Post with that ID not found"}), 404
    post_json = {}
    post_json["title"] = post.title
    post_json["title"] = post.body

    return jsonify({"Message": post_json}), 200
