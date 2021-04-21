"""
Compression picture module
"""
import os
import secrets
from PIL import Image
from app import app


def save_picture(form_picture):
    """
    Save picture function
    """
    random_hex = secrets.token_hex(8)
    f_ext = form_picture.filename.split(".")[-1]
    picture_fn = random_hex + "." + f_ext
    picture_path = os.path.join(app.root_path, "static/img/profiles/" + picture_fn)

    output_size = (256, 256)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn

