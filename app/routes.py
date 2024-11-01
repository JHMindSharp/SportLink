import os
from flask import request, jsonify, Blueprint, render_template, url_for, current_app, redirect, flash
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from werkzeug.utils import secure_filename
from itsdangerous import URLSafeTimedSerializer
from flask_mail import Message
from app import db, mail, bcrypt
from app.models import User, Post
from flask_login import login_user, current_user, logout_user, login_required

# Créer un Blueprint pour les routes principales
bp = Blueprint('main', __name__)

@bp.route('/')
def index():
    """Landing page with signup form."""
    return render_template('index.html')

@bp.route('/posts', methods=['GET'])
def get_posts():
    posts = Post.query.all()
    return jsonify([{"id": post.id, "content": post.content, "created_at": post.created_at} for post in posts])

@bp.route('/posts', methods=['POST'])
@jwt_required()
def create_post():
    user_id = get_jwt_identity()
    data = request.get_json()
    new_post = Post(user_id=user_id, content=data['content'])
    db.session.add(new_post)
    db.session.commit()
    return jsonify({"message": "Post created successfully"}), 201

@bp.route('/register', methods=['POST'])
def register():
    username = request.form.get('username')
    email = request.form.get('email')
    password = request.form.get('password')
    profile_image = None

    if not username or not email or not password:
        return jsonify({"error": "Username, email, and password are required."}), 400

    # Vérifiez que le mot de passe n'est pas vide
    if len(password.strip()) == 0:
        return jsonify({"error": "Password cannot be empty."}), 400

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
    username = request.form.get('username')
    password = request.form.get('password')

    if not username or not password:
        return jsonify({"error": "Username and password are required."}), 400

    user = User.query.filter_by(username=username).first()
    if user is None or not user.check_password(password):
        return jsonify({"error": "Invalid username or password."}), 400

    login_user(user)
    return jsonify({"message": "Login successful."}), 200

@bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash("Vous avez été déconnecté.", "info")
    return redirect(url_for('main.index'))

@bp.errorhandler(404)
def not_found_error(error):
    return jsonify({"error": "Not found"}), 404

@bp.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return jsonify({"error": "Internal server error"}), 500

# Email-related functions
def send_email(subject, recipients, html_body):
    msg = Message(subject, recipients=recipients)
    msg.html = html_body
    mail.send(msg)

def send_confirmation_email(user_email):
    s = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
    token = s.dumps(user_email, salt='email-confirm-salt')
    confirm_url = url_for('main.confirm_email', token=token, _external=True)
    html = render_template('confirm_email.html', confirm_url=confirm_url)
    send_email('Please confirm your email', [user_email], html)

def send_password_reset_email(user_email):
    s = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
    token = s.dumps(user_email, salt='password-reset-salt')
    reset_url = url_for('main.reset_password', token=token, _external=True)
    html = render_template('reset_password.html', reset_url=reset_url)
    send_email('Password reset requested', [user_email], html)

@bp.route('/confirm/<token>')
def confirm_email(token):
    s = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
    try:
        email = s.loads(token, salt='email-confirm-salt', max_age=3600)
    except Exception:
        flash("The confirmation link is invalid or has expired.", "danger")
        return redirect(url_for('main.index'))

    user = User.query.filter_by(email=email).first_or_404()
    if user.email_confirmed:
        flash("Your email is already confirmed.", "info")
    else:
        user.email_confirmed = True
        db.session.commit()
        flash("Your email has been confirmed! You can now log in.", "success")

    return redirect(url_for('main.index'))

@bp.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
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
        flash("Password has been reset!", "success")
        return redirect(url_for('main.index'))

    return render_template('reset_password.html')

@bp.route('/create_profile', methods=['GET', 'POST'])
@login_required
def create_profile():
    if request.method == 'POST':
        user = User.query.get(current_user.id)

        if not user:
            flash("Utilisateur non trouvé.", "danger")
            return redirect(url_for('main.index'))

        user.age = request.form.get('age')
        user.city = request.form.get('city')
        user.country = request.form.get('country')
        user.sex = request.form.get('sex')

        if 'profile_image' in request.files:
            file = request.files['profile_image']
            if file:
                filename = secure_filename(file.filename)
                profile_image = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
                file.save(profile_image)
                user.profile_image = profile_image

        user.profile_completed = True
        db.session.commit()

        flash("Profil créé avec succès !", "success")
        return redirect(url_for('main.profile'))

    return render_template('create_profile.html')

@bp.route('/profile', methods=['GET'])
@login_required
def profile():
    user = User.query.get(current_user.id)
    if not user:
        flash("Utilisateur non trouvé.", "danger")
        return redirect(url_for('main.index'))

    return render_template('profile.html', user=user)
