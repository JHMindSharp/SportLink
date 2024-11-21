"""
app/messages/routes.py

This module defines routes for messaging functionalities in the SportLink application.
It includes features such as viewing the inbox and sending messages between users.

Components:
- `inbox`: Route for viewing received messages.
- `send_message`: Route for sending a message to another user.
"""

from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from app.models import Message, User
from app.extensions import db

# Define the Blueprint for messaging-related routes
messages_bp = Blueprint('messages', __name__, template_folder='templates/messages')

@messages_bp.route('/inbox', methods=['GET'])
@login_required
def inbox():
    """
    Displays the inbox with all messages received by the current user.

    - Retrieves all messages where the recipient is the current user.
    - Orders messages by timestamp in descending order.

    Returns:
    - Rendered 'inbox.html' template with the user's messages.
    """
    messages = Message.query.filter_by(recipient_id=current_user.id).order_by(Message.timestamp.desc()).all()
    return render_template('messages/inbox.html', messages=messages)

@messages_bp.route('/send_message/<int:user_id>', methods=['GET', 'POST'])
@login_required
def send_message(user_id):
    """
    Handles sending a message to another user.

    GET:
    - Renders the message form for composing a new message.

    POST:
    - Sends the message if the form submission is valid.
    - Validates that the message body is not empty.
    - Saves the message to the database.

    Parameters:
    - user_id: ID of the recipient user.

    Returns:
    - On GET: Rendered 'send_message.html' template with the recipient's details.
    - On POST: Redirects to the inbox after the message is successfully sent.
    """
    # Retrieve the recipient user by their ID
    recipient = User.query.get_or_404(user_id)

    if request.method == 'POST':
        body = request.form.get('body')
        # Check if the message body is empty
        if not body:
            flash("Le message ne peut pas être vide.", "danger")
            return redirect(url_for('messages.send_message', user_id=user_id))
        
        # Create and save the new message
        message = Message(sender_id=current_user.id, recipient_id=recipient.id, body=body)
        db.session.add(message)
        db.session.commit()
        
        flash("Message envoyé avec succès.", "success")
        return redirect(url_for('messages.inbox'))

    return render_template('messages/send_message.html', recipient=recipient)
