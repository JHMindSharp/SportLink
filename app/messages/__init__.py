"""
app/messages/__init__.py

This module initializes the 'messages' Blueprint for handling messaging-related functionalities in the application.

Components:
- `messages_bp`: Blueprint instance for messaging-related routes.
- Import of `routes`: Registers the routes related to messaging.
"""

from flask import Blueprint

# Define the Blueprint for messaging-related functionalities
messages_bp = Blueprint('messages', __name__)

# Import routes to register them with the Blueprint
from app.messages import routes
