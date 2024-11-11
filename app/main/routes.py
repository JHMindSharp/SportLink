import os
from flask import Blueprint, render_template, jsonify, send_from_directory, current_app, redirect, url_for
from flask_login import current_user
from app.extensions import db
from app.auth.forms import RegistrationForm, LoginForm

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    if current_user.is_authenticated:
        return redirect(url_for('profile.profile'))
    register_form = RegistrationForm()
    login_form = LoginForm()
    return render_template('home.html', register_form=register_form, login_form=login_form)

@main_bp.app_errorhandler(404)
def not_found_error(error):
    register_form = RegistrationForm()
    login_form = LoginForm()
    return render_template('404.html', register_form=register_form, login_form=login_form), 404

@main_bp.app_errorhandler(500)
def internal_error(error):
    db.session.rollback()
    register_form = RegistrationForm()
    login_form = LoginForm()
    return render_template('500.html', register_form=register_form, login_form=login_form), 500

@main_bp.route('/uploads/<path:filename>')
def uploaded_file(filename):
    return send_from_directory(current_app.config['UPLOAD_FOLDER'], filename)

@main_bp.route('/privacy_policy')
def privacy_policy():
    return render_template('main/privacy_policy.html')
