"""
app/auth/utils.py

This module contains utility functions for user management in the authentication system.
It includes functionalities for password reset emails, token generation, and user registration for OAuth providers.

Components:
- `send_password_reset_email`: Sends a password reset email to the user.
- `generate_reset_token`: Generates a secure token for password reset.
- `register_user_if_new`: Registers a new user if they don't already exist in the database, typically for OAuth providers.
"""

from app.models import User
from app.extensions import db, mail
from flask_mail import Message
from flask import url_for, current_app
from itsdangerous import URLSafeTimedSerializer

def send_password_reset_email(user):
    """
    Sends a password reset email to the specified user.

    Parameters:
    - user: The User object representing the recipient.

    The email includes a secure token and a link for resetting the password.
    """
    token = generate_reset_token(user.email)
    msg = Message('Réinitialisation du mot de passe', recipients=[user.email])
    reset_url = url_for('auth.reset_password', token=token, _external=True)
    msg.body = f'Pour réinitialiser votre mot de passe, cliquez sur le lien suivant : {reset_url}'
    mail.send(msg)

def generate_reset_token(email):
    """
    Generates a secure token for password reset based on the user's email.

    Parameters:
    - email: The user's email address used to create the token.

    Returns:
    - A secure token that can be used to validate password reset requests.
    """
    serializer = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
    return serializer.dumps(email, salt='password-reset-salt')

def register_user_if_new(provider, provider_id, email=None, username=None):
    """
    Checks if a user exists for a given OAuth provider and provider ID. If not, registers the user.

    Parameters:
    - provider: The name of the OAuth provider (e.g., 'facebook', 'strava').
    - provider_id: The unique ID provided by the OAuth provider for the user.
    - email: Optional email address of the user.
    - username: Optional username. If not provided, defaults to a combination of provider and provider ID.

    Returns:
    - The User object for the existing or newly created user.
    """
    user = User.query.filter_by(provider=provider, provider_id=provider_id).first()

    if not user:
        user = User(
            provider=provider,
            provider_id=provider_id,
            email=email,
            username=username or f"{provider}_{provider_id}"
        )
        db.session.add(user)
        db.session.commit()

    return user
