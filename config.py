import os

class Config:
    """Base config class."""
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(os.path.abspath(os.path.dirname(__file__)), 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    UPLOAD_FOLDER = os.path.join(
        os.path.abspath(os.path.dirname(__file__)), 'uploads')

    # Flask-Mail configuration with Gmail
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = 'jonathanhuybrechts@gmail.com'  # Remplacez par votre adresse email
    MAIL_PASSWORD = 'gjwn qbey rjla uwic'  # Remplacez par le mot de passe d'application
    MAIL_DEFAULT_SENDER = 'jonathanhuybrechts@gmail.com'
