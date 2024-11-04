from flask import Blueprint, request, render_template, redirect, url_for, flash, jsonify, current_app, send_from_directory
from flask_login import login_required, current_user
from app.models import User, Sport, Rating, Post
from app.extensions import db
from datetime import datetime
import os
from werkzeug.utils import secure_filename

profile_bp = Blueprint('profile', __name__)

@profile_bp.route('/create_profile', methods=['GET', 'POST'])
@login_required
def create_profile():
    if request.method == 'POST':
        user = User.query.get(current_user.id)

        # Récupération des données du formulaire
        user.country = request.form.get('country')
        user.city = request.form.get('city')
        user.address = request.form.get('address')
        user.postal_code = request.form.get('postal_code')
        user.sex = request.form.get('sex')
        
        # Conversion de la date de naissance
        birth_date_str = request.form.get('birth_date')
        if birth_date_str:
            try:
                user.birth_date = datetime.strptime(birth_date_str, '%Y-%m-%d').date()
            except ValueError:
                flash("Invalid birth date format. Use YYYY-MM-DD.", "danger")
                return redirect(url_for('profile.create_profile'))

        user.phone = request.form.get('phone')
        user.display_phone = request.form.get('display_phone') == 'on'
        user.display_email = request.form.get('display_email') == 'on'
        user.profile_completed = True

        db.session.commit()
        flash("Profile created successfully!", "success")
        return redirect(url_for('profile.profile'))
    
    return render_template('profile/create_profile.html')

@profile_bp.route('/profile', methods=['GET'])
@login_required
def profile():
    user = User.query.get(current_user.id)
    if not user:
        flash("User not found.", "danger")
        return redirect(url_for('main.index'))
    
    # Calcul de la note moyenne
    average_rating = user.average_rating
    total_ratings = user.ratings_received.count()
    posts = user.posts.order_by(Post.created_at.desc()).all()

    return render_template('profile/profile.html', user=user, average_rating=average_rating, total_ratings=total_ratings, posts=posts)

@profile_bp.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    user = User.query.get(current_user.id)
    
    if request.method == 'POST':
        # Mise à jour des informations du profil
        user.username = request.form.get('username', user.username)
        user.email = request.form.get('email', user.email)
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
                flash("Invalid birth date format. Use YYYY-MM-DD.", "danger")
                return redirect(url_for('profile.edit_profile'))

        user.phone = request.form.get('phone', user.phone)
        user.display_phone = request.form.get('display_phone') == 'on'
        user.display_email = request.form.get('display_email') == 'on'

        # Gérer les sports sélectionnés
        selected_sport_ids = request.form.getlist('sports')
        if selected_sport_ids:
            user.sports = [Sport.query.get(int(sport_id)) for sport_id in selected_sport_ids]

        # Gestion du téléchargement de l'image de profil
        if 'profile_image' in request.files:
            profile_image = request.files['profile_image']
            if profile_image.filename != '':
                filename = secure_filename(profile_image.filename)
                profile_image_path = os.path.join(current_app.config['UPLOAD_FOLDER'], 'profiles', filename)
                profile_image.save(profile_image_path)
                user.profile_image = filename  # On enregistre uniquement le nom du fichier

        # Gestion du téléchargement de l'image de couverture
        if 'cover_image' in request.files:
            cover_image = request.files['cover_image']
            if cover_image.filename != '':
                filename = secure_filename(cover_image.filename)
                cover_image_path = os.path.join(current_app.config['UPLOAD_FOLDER'], 'covers', filename)
                cover_image.save(cover_image_path)
                user.cover_image = filename  # On enregistre uniquement le nom du fichier

        db.session.commit()
        flash("Profile updated successfully.", "success")
        return redirect(url_for('profile.profile'))

    sports = Sport.query.all()
    return render_template('profile/edit_profile.html', user=user, sports=sports)

@profile_bp.route('/rate_user/<int:user_id>', methods=['POST'])
@login_required
def rate_user(user_id):
    rating_value = int(request.form.get('rating'))
    
    if rating_value < 1 or rating_value > 5:
        return jsonify({"error": "Invalid rating value."}), 400

    rated_user = User.query.get(user_id)
    if not rated_user:
        return jsonify({"error": "User not found."}), 404

    existing_rating = Rating.query.filter_by(rater_id=current_user.id, rated_id=user_id).first()
    if existing_rating:
        existing_rating.rating = rating_value
        existing_rating.timestamp = datetime.utcnow()
    else:
        new_rating = Rating(rater_id=current_user.id, rated_id=user_id, rating=rating_value)
        db.session.add(new_rating)

    db.session.commit()
    return jsonify({"message": "User rated successfully."}), 200

@profile_bp.route('/add_friend/<int:user_id>', methods=['POST'])
@login_required
def add_friend(user_id):
    user_to_add = User.query.get_or_404(user_id)
    if user_to_add == current_user:
        flash("Vous ne pouvez pas vous ajouter vous-même.", "danger")
        return redirect(url_for('profile.profile', user_id=user_id))

    if current_user.is_friend(user_to_add):
        flash("Vous êtes déjà amis.", "info")
    else:
        current_user.friends.append(user_to_add)
        db.session.commit()
        flash(f"Vous êtes maintenant ami avec {user_to_add.username}.", "success")

    return redirect(url_for('profile.profile', user_id=user_id))

# Méthode dans le modèle User
def is_friend(self, user):
    return self.friends.filter(friends.c.friend_id == user.id).count() > 0
