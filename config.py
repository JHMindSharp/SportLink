import os

class Config:
    """Base config class."""
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(BASE_DIR, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Upload folder configuration
    UPLOAD_FOLDER = os.path.join(BASE_DIR, 'uploads')
    
    # Ensure the upload folders exist
    os.makedirs(os.path.join(UPLOAD_FOLDER, 'profiles'), exist_ok=True)
    os.makedirs(os.path.join(UPLOAD_FOLDER, 'covers'), exist_ok=True)
    os.makedirs(os.path.join(UPLOAD_FOLDER, 'posts', 'images'), exist_ok=True)
    os.makedirs(os.path.join(UPLOAD_FOLDER, 'posts', 'videos'), exist_ok=True)
    os.makedirs(os.path.join(UPLOAD_FOLDER, 'posts', 'music'), exist_ok=True)

    # Flask-Mail configuration with Gmail
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = 'jonathanhuybrechts@gmail.com'  # Remplacez par votre adresse email
    MAIL_PASSWORD = 'gjwn qbey rjla uwic'  # Remplacez par le mot de passe d'application
    MAIL_DEFAULT_SENDER = 'jonathanhuybrechts@gmail.com'
