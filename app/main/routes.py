"""
app/main/routes.py

This module handles the main routes of the SportLink application, including:
- The home page
- Custom error handlers for 404 and 500 errors
- Serving uploaded files
- Displaying the privacy policy

Components:
- `index`: The home page route.
- `not_found_error`: Custom handler for 404 errors.
- `internal_error`: Custom handler for 500 errors.
- `uploaded_file`: Route to serve uploaded files.
- `privacy_policy`: Route to display the privacy policy.
"""

import os
from flask import Blueprint, render_template, jsonify, send_from_directory, current_app, redirect, url_for
from flask_login import current_user
from app.extensions import db
from app.auth.forms import RegistrationForm, LoginForm

# Define the blueprint for main routes
main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    """
    Handles the root URL ('/') of the application.

    - If the user is authenticated, redirects to the profile page.
    - If the user is not authenticated, renders the home page with login and registration forms.

    Returns:
    - Redirect to the profile page if authenticated.
    - Render of 'home.html' with forms if not authenticated.
    """
    if current_user.is_authenticated:
        return redirect(url_for('profile.profile'))
    register_form = RegistrationForm()
    login_form = LoginForm()
    return render_template('home.html', register_form=register_form, login_form=login_form)

@main_bp.app_errorhandler(404)
def not_found_error(error):
    """
    Custom handler for 404 (Not Found) errors.

    - Renders a '404.html' template with login and registration forms.

    Parameters:
    - error: The error object for the 404 exception.

    Returns:
    - Rendered '404.html' with a 404 status code.
    """
    register_form = RegistrationForm()
    login_form = LoginForm()
    return render_template('404.html', register_form=register_form, login_form=login_form), 404

@main_bp.app_errorhandler(500)
def internal_error(error):
    """
    Custom handler for 500 (Internal Server Error) errors.

    - Rolls back the database session to avoid conflicts.
    - Renders a '500.html' template with login and registration forms.

    Parameters:
    - error: The error object for the 500 exception.

    Returns:
    - Rendered '500.html' with a 500 status code.
    """
    db.session.rollback()
    register_form = RegistrationForm()
    login_form = LoginForm()
    return render_template('500.html', register_form=register_form, login_form=login_form), 500

@main_bp.route('/uploads/<path:filename>')
def uploaded_file(filename):
    """
    Serves uploaded files from the configured upload folder.

    Parameters:
    - filename: The name of the file to be served.

    Returns:
    - The requested file from the upload directory.
    """
    return send_from_directory(current_app.config['UPLOAD_FOLDER'], filename)

@main_bp.route('/privacy_policy')
def privacy_policy():
    """
    Displays the privacy policy of the application.

    Returns:
    - Rendered 'privacy_policy.html' template.
    """
    return render_template('main/privacy_policy.html')
