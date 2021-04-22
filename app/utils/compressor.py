"""
Compression picture module
"""
import os
import secrets
from PIL import Image
from app import app


def save_picture(form_picture, model):
    """
    Save picture function
    """
    random_hex = secrets.token_hex(8)
    f_ext = form_picture.filename.split(".")[-1]
    picture_fn = random_hex + "." + f_ext
    if model == "user":
        picture_path = os.path.join(app.root_path, "static/img/profiles/" + picture_fn)
        output_size = (256, 256)
    elif model == "post":
        picture_path = os.path.join(app.root_path, "static/img/posts/" + picture_fn)
        output_size = (512, 256)

    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn

