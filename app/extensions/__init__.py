"""
app/extensions.py

This module initializes and manages the extensions used throughout the SportLink application.
These extensions provide key functionalities such as database management, user authentication, 
password encryption, email handling, and JWT (JSON Web Token) support.

Components:
- `db`: SQLAlchemy for database operations.
- `migrate`: Flask-Migrate for database migrations.
- `bcrypt`: Flask-Bcrypt for password hashing.
- `jwt`: Flask-JWT-Extended for JSON Web Token authentication.
- `mail`: Flask-Mail for email sending.
- `login_manager`: Flask-Login for user session management.
"""

from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from flask_mail import Mail
from flask_login import LoginManager

# ======================
# Extension Initialization
# ======================

# SQLAlchemy: Handles interactions with the database
db = SQLAlchemy()

# Flask-Migrate: Provides database schema migration tools
migrate = Migrate()

# Flask-Bcrypt: Used for hashing passwords
bcrypt = Bcrypt()

# Flask-JWT-Extended: Enables JSON Web Token authentication
jwt = JWTManager()

# Flask-Mail: Provides email-sending capabilities
mail = Mail()

# Flask-Login: Manages user sessions and authentication
login_manager = LoginManager()
