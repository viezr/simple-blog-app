"""
Start point
"""

from app import app, db
from app.models.user import User
from app.models.post import Post


@app.shell_context_processor
def make_shell_context():
    """
    Function for testing projects links without runnig server
    """
    return {"app": app, "db": db, "User": User, "Post": Post}


if __name__ == "__main__":
    app.run()
