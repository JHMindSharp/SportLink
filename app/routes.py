import os
from flask import request, jsonify, Blueprint, render_template, url_for, current_app
from flask_jwt_extended import create_access_token
from werkzeug.utils import secure_filename
from itsdangerous import URLSafeTimedSerializer
from flask_mail import Message
from app import db, mail, bcrypt
from app.models import User

# Create a Blueprint for the main routes
bp = Blueprint('main', __name__)

@bp.route('/', methods=['GET'])
def index():
    """Basic route to check if the app is running."""
    return jsonify({"message": "Welcome to the SportLink API!"})

@bp.route('/register', methods=['POST'])
def register():
    """Register a new user."""
    username = request.form.get('username')
    email = request.form.get('email')
    password = request.form.get('password')
    profile_image = None

    if not username or not email or not password:
        return jsonify({"error": "Username, email, and password are required."}), 400

    if User.query.filter_by(username=username).first():
        return jsonify({"error": "Username already exists."}), 400

    if User.query.filter_by(email=email).first():
        return jsonify({"error": "Email already exists."}), 400

    if 'profile_image' in request.files:
        file = request.files['profile_image']
        if file:
            filename = secure_filename(file.filename)
            profile_image = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
            try:
                file.save(profile_image)
            except Exception as e:
                return jsonify({"error": str(e)}), 500

    user = User(username=username, email=email)
    user.set_password(password)
    user.profile_image = profile_image
    db.session.add(user)
    db.session.commit()

    send_confirmation_email(user.email)
    return jsonify({
        "message": "User registered successfully! Please check your email to confirm your registration."
    }), 201

@bp.route('/login', methods=['POST'])
def login():
    """Login an existing user."""
    email = request.form.get('email')
    password = request.form.get('password')

    current_app.logger.info(f"Received login request for email: {email}")

    if not email or not password:
        current_app.logger.error("Email and password are required.")
        return jsonify({"error": "Email and password are required."}), 400

    user = User.query.filter_by(email=email).first()
    if user is None or not user.check_password(password):
        current_app.logger.error("Invalid email or password.")
        return jsonify({"error": "Invalid email or password."}), 400

    access_token = create_access_token(identity=user.id)
    current_app.logger.info(f"User {email} logged in successfully.")
    return jsonify({
        "message": "User logged in successfully!",
        "access_token": access_token
    }), 200

@bp.errorhandler(404)
def not_found_error(error):
    """Handle 404 errors."""
    return jsonify({"error": "Not found"}), 404

@bp.errorhandler(500)
def internal_error(error):
    """Handle 500 errors."""
    db.session.rollback()
    return jsonify({"error": "Internal server error"}), 500

@bp.route('/update_profile', methods=['POST'])
def update_profile():
    """Update an existing user's profile."""
    username = request.form.get('username')
    email = request.form.get('email')
    new_password = request.form.get('new_password')
    profile_image = None

    user = User.query.filter_by(username=username).first()
    if user is None:
        return jsonify({"error": "User not found."}), 404

    if email:
        user.email = email
    if new_password:
        user.set_password(new_password)

    if 'profile_image' in request.files:
        file = request.files['profile_image']
        if file:
            filename = secure_filename(file.filename)
            profile_image = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
            try:
                file.save(profile_image)
                user.profile_image = profile_image
            except Exception as e:
                return jsonify({"error": str(e)}), 500

    db.session.commit()
    return jsonify({"message": "User profile updated successfully!"}), 200

@bp.route('/search_users', methods=['GET'])
def search_users():
    """Search users by username."""
    query = request.args.get('query', '')
    if not query:
        return jsonify({"error": "Query parameter is required."}), 400

    users = User.query.filter(User.username.ilike(f"%{query}%")).all()
    result = [
        {
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "profile_image": user.profile_image
        }
        for user in users
    ]

    return jsonify(result), 200

@bp.route('/delete_user', methods=['DELETE'])
def delete_user():
    """Delete an existing user."""
    username = request.form.get('username')

    user = User.query.filter_by(username=username).first()
    if user is None:
        return jsonify({"error": "User not found."}), 404

    send_deletion_email(user.email)
    db.session.delete(user)
    db.session.commit()
    return jsonify({"message": "User deleted successfully!"}), 200

def send_email(subject, recipients, html_body):
    """Send an email using Flask-Mail."""
    msg = Message(subject, recipients=recipients)
    msg.html = html_body
    mail.send(msg)

def send_confirmation_email(user_email):
    """Send confirmation email to new user."""
    s = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
    token = s.dumps(user_email, salt='email-confirm-salt')
    confirm_url = url_for('main.confirm_email', token=token, _external=True)
    html = render_template('confirm_email.html', confirm_url=confirm_url)
    send_email('Please confirm your email', [user_email], html)

def send_deletion_email(user_email):
    """Send account deletion email to user."""
    html = render_template('account_deleted.html')
    send_email('Your account has been deleted', [user_email], html)

def send_password_reset_email(user_email):
    """Send password reset email to user."""
    s = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
    token = s.dumps(user_email, salt='password-reset-salt')
    reset_url = url_for('main.reset_password', token=token, _external=True)
    html = render_template('reset_password.html', reset_url=reset_url)
    send_email('Password reset requested', [user_email], html)

@bp.route('/confirm/<token>')
def confirm_email(token):
    """Confirm the user's email address."""
    s = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
    try:
        email = s.loads(token, salt='email-confirm-salt', max_age=3600)
    except Exception:
        return jsonify({"error": "The confirmation link is invalid or has expired."}), 400

    user = User.query.filter_by(email=email).first_or_404()
    user.email_confirmed = True
    db.session.commit()
    return jsonify({"message": "Email confirmed!"})

@bp.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    """Reset the user's password."""
    s = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
    try:
        email = s.loads(token, salt='password-reset-salt', max_age=3600)
    except Exception:
        return jsonify({"error": "The reset link is invalid or has expired."}), 400

    user = User.query.filter_by(email=email).first_or_404()
    if request.method == 'POST':
        new_password = request.form['password']
        user.set_password(new_password)
        db.session.commit()
        return jsonify({"message": "Password has been reset!"})

    return render_template('reset_password.html')
