import os


class Config:
    """Base config class."""

    # Secret key for session management and other security-related needs.
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'

    # Database URI for SQLAlchemy. Default to a local SQLite database if not
    # provided.
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(
            os.path.abspath(os.path.dirname(__file__)), 'app.db')

    # Disable SQLAlchemy event system to save resources.
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Directory to store uploaded files.
    UPLOAD_FOLDER = os.path.join(
        os.path.abspath(os.path.dirname(__file__)), 'uploads')
