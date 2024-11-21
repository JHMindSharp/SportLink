"""
app/news_feed/routes.py

This module defines routes related to the news feed functionality in the SportLink application.
The news feed allows users to view posts from their friends and public posts.

Components:
- `news_feed`: Displays the news feed with posts from friends, the current user, and public posts.
"""

from flask import Blueprint, render_template, request
from flask_login import login_required, current_user
from app.models import Post
from app.extensions import db

# Define the Blueprint for news feed-related routes
news_feed_bp = Blueprint('news_feed', __name__, template_folder='templates/news_feed')

@news_feed_bp.route('/', methods=['GET'])
@login_required
def news_feed():
    """
    Displays the news feed for the logged-in user.

    - Retrieves posts created by the current user, their friends, and public posts.
    - Orders posts by creation date in descending order.

    Process:
    - Fetch the IDs of the current user's friends.
    - Include the current user's ID in the list.
    - Query posts that are either:
      1. Created by the current user or their friends, and
      2. Visible as public posts or specific to the current user.

    Returns:
    - Rendered 'news_feed.html' template with the list of posts.
    """
    # Get IDs of the current user's friends
    friends_ids = [friend.id for friend in current_user.friends]

    # Include the current user's ID in the list of post sources
    friends_ids.append(current_user.id)

    # Query the database for posts from the current user, their friends, and public posts
    posts = Post.query.filter(
        (Post.user_id.in_(friends_ids)) &  # Posts from the current user and friends
        ((Post.visibility == 'public') | (Post.user_id == current_user.id))  # Public or specific to the user
    ).order_by(Post.created_at.desc()).all()

    # Render the news feed template with the retrieved posts
    return render_template('news_feed/news_feed.html', posts=posts)
