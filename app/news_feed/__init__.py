"""
app/news_feed/__init__.py

This module initializes the 'news_feed' Blueprint for handling the news feed functionality in the application.

Components:
- `news_feed_bp`: Blueprint instance for the news feed-related routes.
- Import of `routes`: Registers the routes related to the news feed.
"""

from flask import Blueprint

# Define the Blueprint for news feed-related functionalities
news_feed_bp = Blueprint('news_feed', __name__)

# Import routes to register them with the Blueprint
from app.news_feed import routes
