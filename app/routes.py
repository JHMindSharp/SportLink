import os
from flask import request, jsonify, Blueprint, render_template, url_for, current_app, redirect, flash, send_from_directory
from datetime import datetime
from flask_mail import Message
from app import mail, db, bcrypt
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from werkzeug.utils import secure_filename
from itsdangerous import URLSafeTimedSerializer
from app.models import User, Post, Sport, Rating, Message
from flask_login import login_user, current_user, logout_user, login_required
from sqlalchemy.exc import SQLAlchemyError
from app.extensions import db, mail, bcrypt
from . import bcrypt

bp = Blueprint('main', __name__)

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'mp4', 'mp3'}

def allowed_file(filename):
    """Check if the file has an allowed extension."""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@bp.route('/')
def index():
    """Landing page with signup form."""
    return render_template('index.html')

@bp.route('/posts', methods=['GET'])
def get_posts():
    posts = Post.query.all()
    return jsonify([{
        "id": post.id,
        "content_type": post.content_type,
        "title": post.title,
        "subtitle": post.subtitle,
        "content": post.content,
        "image": post.image,
        "video": post.video,
        "music": post.music,
        "created_at": post.created_at,
        "author": post.author.username
    } for post in posts])

@bp.route('/posts', methods=['POST'])
@jwt_required()
def create_post_api():
    user_id = get_jwt_identity()
    data = request.get_json()
    new_post = Post(
        user_id=user_id,
        content_type=data.get('content_type', 'free'),
        title=data.get('title'),
        subtitle=data.get('subtitle'),
        content=data['content']
    )
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

    # Check that password is not empty
    if len(password.strip()) == 0:
        return jsonify({"error": "Password cannot be empty."}), 400

    if User.query.filter_by(username=username).first():
        return jsonify({"error": "Username already exists."}), 400

    if User.query.filter_by(email=email).first():
        return jsonify({"error": "Email already exists."}), 400

    if 'profile_image' in request.files:
        file = request.files['profile_image']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            profile_image_path = os.path.join(current_app.config['UPLOAD_FOLDER'], 'profiles', filename)
            os.makedirs(os.path.dirname(profile_image_path), exist_ok=True)
            file.save(profile_image_path)
            profile_image = os.path.join('profiles', filename)

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

        user.country = request.form.get('country')
        user.city = request.form.get('city')
        user.address = request.form.get('address')
        user.postal_code = request.form.get('postal_code')
        user.sex = request.form.get('sex')
        birth_date_str = request.form.get('birth_date')
        if birth_date_str:
            try:
                user.birth_date = datetime.strptime(birth_date_str, '%Y-%m-%d').date()
            except ValueError:
                flash("Invalid birth date.", "danger")
                return redirect(url_for('main.create_profile'))

        user.phone = request.form.get('phone')
        user.display_phone = request.form.get('display_phone') == 'on'
        user.display_email = request.form.get('display_email') == 'on'

        # Handle profile image upload
        if 'profile_image' in request.files:
            file = request.files['profile_image']
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                profile_image_path = os.path.join(current_app.config['UPLOAD_FOLDER'], 'profiles', filename)
                os.makedirs(os.path.dirname(profile_image_path), exist_ok=True)
                file.save(profile_image_path)
                user.profile_image = os.path.join('profiles', filename)

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

    # Calculate average rating
    average_rating = user.average_rating
    total_ratings = user.ratings_received.count()
    posts = user.posts.order_by(Post.created_at.desc()).all()
    return render_template(
        'profile.html',
        user=user,
        average_rating=average_rating,
        total_ratings=total_ratings,
        posts=posts
    )

@bp.route('/update_profile', methods=['POST'])
@login_required
def update_profile():
    user = User.query.get(current_user.id)

    # Fetch new profile data from form
    user.country = request.form.get('country', user.country)
    user.city = request.form.get('city', user.city)
    user.address = request.form.get('address', user.address)
    user.postal_code = request.form.get('postal_code', user.postal_code)
    user.sex = request.form.get('sex', user.sex)
    birth_date_str = request.form.get('birth_date')
    if birth_date_str:
        try:
            user.birth_date = datetime.strptime(birth_date_str, '%Y-%m-%d').date()
        except ValueError:
            flash("Invalid birth date.", "danger")
            return redirect(url_for('main.edit_profile'))

    user.phone = request.form.get('phone', user.phone)
    user.display_phone = request.form.get('display_phone') == 'on'
    user.display_email = request.form.get('display_email') == 'on'

    # Gérer l'upload de l'image de profil
    if 'profile_image' in request.files:
        file = request.files['profile_image']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            profile_image_path = os.path.join(current_app.config['UPLOAD_FOLDER'], 'profiles', filename)
            os.makedirs(os.path.dirname(profile_image_path), exist_ok=True)
            file.save(profile_image_path)
            # Enregistrer uniquement le chemin relatif dans la base de données
            user.profile_image = os.path.join('profiles', filename)

    # Gérer l'upload de l'image de couverture
    if 'cover_image' in request.files:
        file = request.files['cover_image']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            cover_image_path = os.path.join(current_app.config['UPLOAD_FOLDER'], 'covers', filename)
            os.makedirs(os.path.dirname(cover_image_path), exist_ok=True)
            file.save(cover_image_path)
            # Enregistrer uniquement le chemin relatif dans la base de données
            user.cover_image = os.path.join('covers', filename)


    # Handle sports selection
    selected_sport_ids = request.form.getlist('sports')
    if selected_sport_ids:
        user.sports = []
        for sport_id in selected_sport_ids[:5]:  # Limit to 5 sports
            sport = Sport.query.get(int(sport_id))
            if sport:
                user.sports.append(sport)

    new_email = request.form.get('email')
    if new_email and new_email != user.email:
        # Handle pending email confirmation
        user.pending_email = new_email
        send_email_confirmation(user.pending_email)
        flash("Please confirm your new email address. Check your email for a confirmation link.", "info")

    db.session.commit()
    flash("Profile updated successfully.", "success")
    return redirect(url_for('main.profile'))

def send_email_confirmation(email):
    token = URLSafeTimedSerializer(current_app.config['SECRET_KEY']).dumps(email, salt='email-confirm-salt')
    confirm_url = url_for('main.confirm_email_change', token=token, _external=True)
    html = render_template('confirm_email.html', confirm_url=confirm_url)
    msg = Message("Confirm your new email address", recipients=[email])
    msg.html = html
    mail.send(msg)

@bp.route('/confirm_email_change/<token>')
def confirm_email_change(token):
    try:
        email = URLSafeTimedSerializer(current_app.config['SECRET_KEY']).loads(token, salt='email-confirm-salt', max_age=3600)
    except Exception:
        flash("The confirmation link is invalid or has expired.", "danger")
        return redirect(url_for('main.profile'))

    user = User.query.filter_by(pending_email=email).first_or_404()
    user.email = user.pending_email
    user.pending_email = None
    db.session.commit()

    flash("Your email address has been updated.", "success")
    return redirect(url_for('main.profile'))

@bp.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    if request.method == 'POST':
        user = User.query.get(current_user.id)
        if not user:
            flash("User not found.", "danger")
            return redirect(url_for('main.index'))

        # Update profile fields
        user.username = request.form.get('username', user.username)
        user.country = request.form.get('country', user.country)
        user.city = request.form.get('city', user.city)
        user.sex = request.form.get('sex', user.sex)
        birth_date_str = request.form.get('birth_date')
        if birth_date_str:
            try:
                user.birth_date = datetime.strptime(birth_date_str, '%Y-%m-%d').date()
            except ValueError:
                flash("Invalid birth date.", "danger")
                return redirect(url_for('main.edit_profile'))
        else:
            user.birth_date = user.birth_date

        # Handle profile image upload
        if 'profile_image' in request.files:
            file = request.files['profile_image']
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                profile_image_path = os.path.join(current_app.config['UPLOAD_FOLDER'], 'profiles', filename)
                os.makedirs(os.path.dirname(profile_image_path), exist_ok=True)
                file.save(profile_image_path)
                user.profile_image = os.path.join('profiles', filename)

        # Handle cover image upload
        if 'cover_image' in request.files:
            file = request.files['cover_image']
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                cover_image_path = os.path.join(current_app.config['UPLOAD_FOLDER'], 'covers', filename)
                os.makedirs(os.path.dirname(cover_image_path), exist_ok=True)
                file.save(cover_image_path)
                user.cover_image = os.path.join('covers', filename)

        # Handle sports selection
        selected_sport_ids = request.form.getlist('sports')
        if selected_sport_ids:
            user.sports = []
            for sport_id in selected_sport_ids[:5]:  # Limit to 5 sports
                sport = Sport.query.get(int(sport_id))
                if sport:
                    user.sports.append(sport)

        db.session.commit()
        flash("Profile updated successfully.", "success")
        return redirect(url_for('main.profile'))

    else:
        sports = Sport.query.all()
        return render_template('edit_profile.html', user=current_user, sports=sports)

@bp.route('/rate_user/<int:user_id>', methods=['POST'])
@login_required
def rate_user(user_id):
    rating_value = int(request.form.get('rating'))
    if rating_value < 1 or rating_value > 5:
        return jsonify({"error": "Invalid rating value."}), 400

    rated_user = User.query.get(user_id)
    if not rated_user:
        return jsonify({"error": "User not found."}), 404

    # Check if current_user has already rated this user
    existing_rating = Rating.query.filter_by(rater_id=current_user.id, rated_id=user_id).first()
    if existing_rating:
        existing_rating.rating = rating_value
        existing_rating.timestamp = datetime.utcnow()
    else:
        new_rating = Rating(rater_id=current_user.id, rated_id=user_id, rating=rating_value)
        db.session.add(new_rating)

    db.session.commit()
    return jsonify({"message": "User rated successfully."}), 200

@bp.route('/create_post', methods=['GET', 'POST'])
@login_required
def create_post():
    if request.method == 'POST':
        content_type = request.form.get('content_type')  # 'free' or 'sport'
        title = request.form.get('title')
        subtitle = request.form.get('subtitle')
        content = request.form.get('content')

        # Handle file uploads
        image_file = request.files.get('image')
        video_file = request.files.get('video')
        music_file = request.files.get('music')

        image_path = None
        video_path = None
        music_path = None

        if image_file and allowed_file(image_file.filename):
            filename = secure_filename(image_file.filename)
            image_save_path = os.path.join(current_app.config['UPLOAD_FOLDER'], 'posts', 'images', filename)
            os.makedirs(os.path.dirname(image_save_path), exist_ok=True)
            image_file.save(image_save_path)
            image_path = os.path.join('posts', 'images', filename)

        if video_file and allowed_file(video_file.filename):
            filename = secure_filename(video_file.filename)
            video_save_path = os.path.join(current_app.config['UPLOAD_FOLDER'], 'posts', 'videos', filename)
            os.makedirs(os.path.dirname(video_save_path), exist_ok=True)
            video_file.save(video_save_path)
            video_path = os.path.join('posts', 'videos', filename)

        if music_file and allowed_file(music_file.filename):
            filename = secure_filename(music_file.filename)
            music_save_path = os.path.join(current_app.config['UPLOAD_FOLDER'], 'posts', 'music', filename)
            os.makedirs(os.path.dirname(music_save_path), exist_ok=True)
            music_file.save(music_save_path)
            music_path = os.path.join('posts', 'music', filename)

        new_post = Post(
            user_id=current_user.id,
            content_type=content_type,
            title=title,
            subtitle=subtitle,
            content=content,
            image=image_path,
            video=video_path,
            music=music_path
        )

        db.session.add(new_post)
        db.session.commit()

        flash("Post created successfully.", "success")
        return redirect(url_for('main.profile'))

    else:
        return render_template('create_post.html')

@bp.route('/delete_post/<int:post_id>', methods=['POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get(post_id)
    if not post or post.user_id != current_user.id:
        flash("Post not found or you do not have permission to delete it.", "danger")
        return redirect(url_for('main.profile'))

    try:
        db.session.delete(post)
        db.session.commit()
        flash("Post deleted successfully.", "success")
    except SQLAlchemyError:
        db.session.rollback()
        flash("An error occurred while deleting the post.", "danger")

    return redirect(url_for('main.profile'))

@bp.route('/uploads/<path:filename>')
def uploaded_file(filename):
    return send_from_directory(current_app.config['UPLOAD_FOLDER'], filename)

@bp.route('/news_feed')
@login_required
def news_feed():
    # Obtenir les posts de l'utilisateur et de ses amis
    friends_ids = [friend.id for friend in current_user.friends()]
    posts = Post.query.filter(Post.user_id.in_(friends_ids + [current_user.id])).order_by(Post.created_at.desc()).all()
    return render_template('news_feed.html', posts=posts)

def inbox():
    messages = current_user.received_messages.order_by(Message.timestamp.desc()).all()
    return render_template('messages/inbox.html', messages=messages)

@bp.route('/messages/send/<int:recipient_id>', methods=['GET', 'POST'])
@login_required
def send_message(recipient_id):
    recipient = User.query.get_or_404(recipient_id)
    if request.method == 'POST':
        body = request.form['body']
        if body:
            msg = Message(sender=current_user, recipient=recipient, body=body)
            db.session.add(msg)
            db.session.commit()
            flash('Message envoyé.', 'success')
            return redirect(url_for('messages.inbox'))
        else:
            flash('Le message ne peut pas être vide.', 'danger')
    return render_template('messages/send_message.html', recipient=recipient)
