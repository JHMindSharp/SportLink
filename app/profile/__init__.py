"""
app/profile/__init__.py

This module initializes the 'profile' Blueprint, which handles functionalities related to user profiles in the application.

Components:
- `profile_bp`: Blueprint instance for profile-related routes.
- Import of `routes`: Registers the routes associated with the profile Blueprint.
"""

from flask import Blueprint

# Define the Blueprint for profile-related functionalities
profile_bp = Blueprint('profile', __name__)

# Import routes to register them with the Blueprint
from app.profile import routes
