"""
Errors handler module
"""
from flask import flash, render_template
from flask_babel import _
from app import app


@app.errorhandler(404)
def error_404(error):
    """
    Render custom template for 404 error
    """
    flash(_("Error 404"), "warning")
    return render_template("errors/404.html", title="404 Bad request")


@app.errorhandler(403)
def error_403(error):
    """
    Render custom template for 403 error
    """
    flash(_("Error 403"), "warning")
    return render_template("errors/403.html", title="403 Permission")


@app.errorhandler(500)
def error_500(error):
    """
    Render custom template for 500 error
    """
    flash(_("Error 500"), "warning")
    return render_template("errors/500.html", title="500 Server error")
