"""
app/auth/__init__.py

This module initializes the 'auth' Blueprint for the authentication-related routes in the application.
The Blueprint allows for modular organization of the code and keeps all authentication routes grouped together.

Components:
- `auth_bp`: Blueprint instance for authentication.
- `routes`: Imports the authentication routes to register them with the Blueprint.
"""

from flask import Blueprint

# Define the 'auth' Blueprint to handle authentication-related routes
auth_bp = Blueprint('auth', __name__)

# Import the routes associated with the 'auth' Blueprint
from app.auth import routes
