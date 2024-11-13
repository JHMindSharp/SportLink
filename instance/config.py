# Configuration file for the Flask application
# Fichier de configuration pour l'application Flask

import os

# General configuration
# Configuration générale
SECRET_KEY = os.environ.get('SECRET_KEY', 'you-will-never-guess')  # Secret key for session management
BASE_DIR = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))  # Base directory path
SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', 'sqlite:///' + os.path.join(BASE_DIR, 'app.db'))  # Database URI
SQLALCHEMY_TRACK_MODIFICATIONS = False  # Disable modification tracking to save resources

# Directory for uploads
# Dossier pour les téléchargements
UPLOAD_FOLDER = os.path.join(BASE_DIR, 'uploads')

# Ensure the upload folders exist
# Assure l'existence des dossiers de téléchargement
os.makedirs(os.path.join(UPLOAD_FOLDER, 'profiles'), exist_ok=True)
os.makedirs(os.path.join(UPLOAD_FOLDER, 'covers'), exist_ok=True)
os.makedirs(os.path.join(UPLOAD_FOLDER, 'posts', 'images'), exist_ok=True)
os.makedirs(os.path.join(UPLOAD_FOLDER, 'posts', 'videos'), exist_ok=True)
os.makedirs(os.path.join(UPLOAD_FOLDER, 'posts', 'music'), exist_ok=True)

# Flask-Mail configuration with Gmail
# Configuration de Flask-Mail avec Gmail
MAIL_SERVER = 'smtp.gmail.com'
MAIL_PORT = 587
MAIL_USE_TLS = True
MAIL_USERNAME = os.environ.get('MAIL_USERNAME')  # Username for SMTP
MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')  # Password for SMTP
MAIL_DEFAULT_SENDER = os.environ.get('MAIL_DEFAULT_SENDER')  # Default sender email address

# Facebook OAuth Configuration
# Configuration OAuth pour Facebook
FACEBOOK_OAUTH_CLIENT_ID = os.environ.get('FACEBOOK_OAUTH_CLIENT_ID')  # Client ID for Facebook
FACEBOOK_OAUTH_CLIENT_SECRET = os.environ.get('FACEBOOK_OAUTH_CLIENT_SECRET')  # Client secret for Facebook

# Strava OAuth Configuration
# Configuration OAuth pour Strava
STRAVA_OAUTH_CLIENT_ID = os.environ.get('STRAVA_OAUTH_CLIENT_ID')  # Client ID for Strava
STRAVA_OAUTH_CLIENT_SECRET = os.environ.get('STRAVA_OAUTH_CLIENT_SECRET')  # Client secret for Strava
