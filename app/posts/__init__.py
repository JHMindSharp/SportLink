"""
app/posts/__init__.py

This module initializes the 'posts' Blueprint, which handles functionalities related to user posts in the application.

Components:
- `posts_bp`: Blueprint instance for post-related routes.
- Import of `routes`: Registers the routes related to posts.
"""

from flask import Blueprint

# Define the Blueprint for post-related functionalities
posts_bp = Blueprint('posts', __name__)

# Import routes to register them with the Blueprint
from app.posts import routes
