import os
from flask import request, jsonify, current_app, Blueprint
from flask_jwt_extended import create_access_token
from werkzeug.utils import secure_filename
from app import db
from app.models import User

bp = Blueprint('main', __name__)

@bp.route('/', methods=['GET'])
def index():
    """Basic route to check if the app is running."""
    return jsonify({"message": "Welcome to the SportLink API!"})

@bp.route('/register', methods=['POST'])
def register():
    """Register a new user."""
    username = request.form.get('username')
    password = request.form.get('password')
    profile_image = None

    if not username or not password:
        return jsonify({"error": "Username and password are required."}), 400

    if User.query.filter_by(username=username).first():
        return jsonify({"error": "Username already exists."}), 400

    if 'profile_image' in request.files:
        file = request.files['profile_image']
        if file:
            filename = secure_filename(file.filename)
            profile_image = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
            try:
                file.save(profile_image)
            except Exception as e:
                return jsonify({"error": str(e)}), 500

    user = User(username=username)
    user.set_password(password)
    user.profile_image = profile_image
    db.session.add(user)
    db.session.commit()

    return jsonify({"message": "User registered successfully!"}), 201

@bp.route('/login', methods=['POST'])
def login():
    """Login an existing user."""
    data = request.json
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({"error": "Username and password are required."}), 400

    user = User.query.filter_by(username=username).first()
    if user is None or not user.check_password(password):
        return jsonify({"error": "Invalid username or password."}), 400

    access_token = create_access_token(identity=user.id)
    return jsonify({"message": "User logged in successfully!", "access_token": access_token}), 200

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
    new_password = request.form.get('new_password')
    profile_image = None

    user = User.query.filter_by(username=username).first()

    if user is None:
        return jsonify({"error": "User not found."}), 404

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
    result = [{"id": user.id, "username": user.username, "profile_image": user.profile_image} for user in users]

    return jsonify(result), 200
