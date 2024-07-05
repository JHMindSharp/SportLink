import os
from flask import request, jsonify, current_app, Blueprint
from flask_jwt_extended import create_access_token
from werkzeug.utils import secure_filename
from app import db
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

    # Check if all required fields are provided
    if not username or not email or not password:
        return jsonify(
            {"error": "Username, email, and password are required."}), 400

    # Check if the username or email already exists in the database
    if User.query.filter_by(
            username=username).first() or User.query.filter_by(
            email=email).first():
        return jsonify({"error": "Username or email already exists."}), 400

    # Save the profile image if provided
    if 'profile_image' in request.files:
        file = request.files['profile_image']
        if file:
            filename = secure_filename(file.filename)
            profile_image = os.path.join(
                current_app.config['UPLOAD_FOLDER'], filename)
            try:
                file.save(profile_image)
            except Exception as e:
                return jsonify({"error": str(e)}), 500

    # Create a new User instance and save to the database
    user = User(username=username, email=email)
    user.set_password(password)
    user.profile_image = profile_image
    db.session.add(user)
    db.session.commit()

    return jsonify({"message": "User registered successfully!"}), 201


@bp.route('/login', methods=['POST'])
def login():
    """Login an existing user."""
    data = request.json
    email = data.get('email')
    password = data.get('password')

    # Check if email and password are provided
    if not email or not password:
        return jsonify({"error": "Email and password are required."}), 400

    # Query the database for the user
    user = User.query.filter_by(email=email).first()
    if user is None or not user.check_password(password):
        return jsonify({"error": "Invalid email or password."}), 400

    # Create an access token for the user
    access_token = create_access_token(identity=user.id)
    return jsonify({"message": "User logged in successfully!",
                   "access_token": access_token}), 200


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

    # Query the database for the user
    user = User.query.filter_by(username=username).first()

    # Check if the user exists
    if user is None:
        return jsonify({"error": "User not found."}), 404

    # Update the user's email and password if provided
    if email:
        user.email = email
    if new_password:
        user.set_password(new_password)

    # Save the new profile image if provided
    if 'profile_image' in request.files:
        file = request.files['profile_image']
        if file:
            filename = secure_filename(file.filename)
            profile_image = os.path.join(
                current_app.config['UPLOAD_FOLDER'], filename)
            try:
                file.save(profile_image)
                user.profile_image = profile_image
            except Exception as e:
                return jsonify({"error": str(e)}), 500

    # Commit the changes to the database
    db.session.commit()

    return jsonify({"message": "User profile updated successfully!"}), 200


@bp.route('/search_users', methods=['GET'])
def search_users():
    """Search users by username."""
    query = request.args.get('query', '')
    if not query:
        return jsonify({"error": "Query parameter is required."}), 400

    users = User.query.filter(User.username.ilike(f"%{query}%")).all()
    result = [{"id": user.id, "username": user.username,
               "email": user.email,
               "profile_image": user.profile_image} for user in users]

    return jsonify(result), 200


@bp.route('/delete_user', methods=['DELETE'])
def delete_user():
    """Delete an existing user."""
    username = request.form.get('username')

    # Query the database for the user
    user = User.query.filter_by(username=username).first()

    # Check if the user exists
    if user is None:
        return jsonify({"error": "User not found."}), 404

    # Delete the user from the database
    db.session.delete(user)
    db.session.commit()

    return jsonify({"message": "User deleted successfully!"}), 200
