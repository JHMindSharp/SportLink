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
    MAIL_USERNAME = 'jonathanhuybrechts@gmail.com'
    MAIL_PASSWORD = 'gjwn qbey rjla uwic'
    MAIL_DEFAULT_SENDER = 'jonathanhuybrechts@gmail.com'

    # Facebook OAuth Configuration
    FACEBOOK_OAUTH_CLIENT_ID = '1286943945646152'  # Remplacez par votre ID client Facebook
    FACEBOOK_OAUTH_CLIENT_SECRET = '8ca793277b7f8e073009091327755e3c'  # Remplacez par votre secret client Facebook
    STRAVA_OAUTH_CLIENT_ID = '139086'
    STRAVA_OAUTH_CLIENT_SECRET = '37a89dffff059526e9c4d62ab49b47a88372972c'
