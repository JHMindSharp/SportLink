from decouple import config
import os

SECRET_KEY = config('SECRET_KEY')
BASE_DIR = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
SQLALCHEMY_DATABASE_URI = config('DATABASE_URL')
SQLALCHEMY_TRACK_MODIFICATIONS = False
UPLOAD_FOLDER = os.path.join(BASE_DIR, 'uploads')

# Ensure the upload folders exist
os.makedirs(os.path.join(UPLOAD_FOLDER, 'profiles'), exist_ok=True)
os.makedirs(os.path.join(UPLOAD_FOLDER, 'covers'), exist_ok=True)
os.makedirs(os.path.join(UPLOAD_FOLDER, 'posts', 'images'), exist_ok=True)
os.makedirs(os.path.join(UPLOAD_FOLDER, 'posts', 'videos'), exist_ok=True)
os.makedirs(os.path.join(UPLOAD_FOLDER, 'posts', 'music'), exist_ok=True)

# Flask-Mail configuration with Gmail
MAIL_SERVER = config('MAIL_SERVER', default='smtp.gmail.com')
MAIL_PORT = config('MAIL_PORT', default=587, cast=int)
MAIL_USE_TLS = config('MAIL_USE_TLS', default=True, cast=bool)
MAIL_USERNAME = config('MAIL_USERNAME')
MAIL_PASSWORD = config('MAIL_PASSWORD')
MAIL_DEFAULT_SENDER = config('MAIL_DEFAULT_SENDER')

# Facebook OAuth Configuration
FACEBOOK_OAUTH_CLIENT_ID = config('FACEBOOK_OAUTH_CLIENT_ID')
FACEBOOK_OAUTH_CLIENT_SECRET = config('FACEBOOK_OAUTH_CLIENT_SECRET')

# Strava OAuth Configuration
STRAVA_OAUTH_CLIENT_ID = config('STRAVA_OAUTH_CLIENT_ID')
STRAVA_OAUTH_CLIENT_SECRET = config('STRAVA_OAUTH_CLIENT_SECRET')

# Upload configuration
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'mp4', 'mov'}
MAX_CONTENT_LENGTH = 10 * 1024 * 1024  # 10 MB
