"""
app/notifications/routes.py

This module defines routes for managing and displaying notifications in the SportLink application.
It allows users to view a list of their notifications.

Components:
- `list_notifications`: Displays a list of notifications for the logged-in user.
"""

from flask import Blueprint, render_template
from flask_login import login_required, current_user
from app.models import Notification

# Define the Blueprint for notification-related routes
notifications_bp = Blueprint('notifications', __name__)

@notifications_bp.route('/list', methods=['GET'])
@login_required
def list_notifications():
    """
    Displays a list of notifications for the current logged-in user.

    - Fetches the user's notifications from the database.
    - Orders notifications by their timestamp in descending order.

    Returns:
    - Rendered 'list.html' template with the user's notifications.
    """
    # Retrieve the current user's notifications, ordered by the timestamp
    notifications = current_user.notifications.order_by(Notification.timestamp.desc()).all()

    # Render the notifications template with the retrieved notifications
    return render_template('notifications/list.html', notifications=notifications)
