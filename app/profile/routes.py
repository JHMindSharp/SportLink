"""
app/profile/routes.py

This file contains all routes and logic related to user profile management.
"""

from flask import Blueprint, request, render_template, redirect, url_for, flash, jsonify, current_app
from flask_wtf import FlaskForm
from flask_login import login_required, current_user, logout_user
from app.models import User, Sport, Rating, Post, UserSport
from app.extensions import db
from datetime import datetime
import os
from werkzeug.utils import secure_filename
from app.profile.forms import (
    EditProfileForm,
    ChangeEmailForm,
    ChangePasswordForm,
    DeleteAccountForm,
    CompleteProfileForm
)
from app.auth.forms import RegistrationForm, LoginForm
from werkzeug.security import generate_password_hash

profile_bp = Blueprint('profile', __name__)

class EmptyForm(FlaskForm):
    pass

@profile_bp.route('/settings', methods=['GET', 'POST'])
@login_required
def settings():
    change_email_form = ChangeEmailForm()
    change_password_form = ChangePasswordForm()
    delete_account_form = DeleteAccountForm()
    return render_template('profile/settings.html', change_email_form=change_email_form, change_password_form=change_password_form, delete_account_form=delete_account_form)

@profile_bp.route('/change_email', methods=['POST'])
@login_required
def change_email():
    form = ChangeEmailForm()
    if form.validate_on_submit():
        current_user.email = form.email.data
        db.session.commit()
        flash("Votre adresse email a été mise à jour.", "success")
    else:
        flash("Erreur lors de la mise à jour de l'email.", "danger")
    return redirect(url_for('profile.settings'))

@profile_bp.route('/change_password', methods=['POST'])
@login_required
def change_password():
    form = ChangePasswordForm()
    if form.validate_on_submit():
        current_user.set_password(form.new_password.data)
        db.session.commit()
        flash("Votre mot de passe a été mis à jour. Veuillez vous reconnecter.", "success")
        logout_user()  # Déconnecte l'utilisateur après la mise à jour du mot de passe
        return redirect(url_for('auth.login'))
    else:
        flash("Erreur lors de la mise à jour du mot de passe.", "danger")
    return redirect(url_for('profile.settings'))

@profile_bp.route('/delete_account', methods=['POST'])
@login_required
def delete_account():
    form = DeleteAccountForm()
    if form.validate_on_submit():
        user = current_user._get_current_object()  # Obtenir l'instance réelle de l'utilisateur
        if isinstance(user, User):  # Vérification que l'utilisateur est bien de la classe User
            db.session.delete(user)
            db.session.commit()
            logout_user()  # Déconnexion après la suppression de l'utilisateur
            flash("Votre compte a été supprimé.", "success")
            return redirect(url_for('main.index'))
        else:
            flash("Erreur lors de la suppression du compte.", "danger")
    else:
        flash("Erreur lors de la validation du formulaire.", "danger")
    return redirect(url_for('profile.settings'))

@profile_bp.route('/profile', methods=['GET'])
@login_required
def profile():
    user = current_user
    average_rating = user.average_rating
    total_ratings = user.ratings_received.count()
    posts = user.posts.order_by(Post.created_at.desc()).all()
    sports = Sport.query.all()
    form = EmptyForm()
    return render_template(
        'profile/profile.html',
        user=user,
        average_rating=average_rating,
        total_ratings=total_ratings,
        posts=posts,
        sports=sports,
        form=form
    )

@profile_bp.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    user = current_user
    form = EditProfileForm()

    if form.validate_on_submit():
        user.username = form.username.data
        user.email = form.email.data
        user.first_name = form.first_name.data
        user.last_name = form.last_name.data
        user.country = form.country.data
        user.city = form.city.data
        user.address = form.address.data
        user.postal_code = form.postal_code.data
        user.sex = form.sex.data
        user.birth_date = form.birth_date.data
        user.phone = form.phone.data
        user.display_phone = form.display_phone.data
        user.display_email = form.display_email.data
        user.latitude = form.latitude.data
        user.longitude = form.longitude.data

        if form.profile_image.data:
            profile_image = form.profile_image.data
            filename = secure_filename(profile_image.filename)
            profile_image_path = os.path.join(current_app.config['UPLOAD_FOLDER'], 'profiles', filename)
            profile_image.save(profile_image_path)
            user.profile_image = filename

        if form.cover_image.data:
            cover_image = form.cover_image.data
            filename = secure_filename(cover_image.filename)
            cover_image_path = os.path.join(current_app.config['UPLOAD_FOLDER'], 'covers', filename)
            cover_image.save(cover_image_path)
            user.cover_image = filename

        # Update sports and levels
        for sport in Sport.query.all():
            level = request.form.get(f'sport_{sport.id}')
            if level:
                level = int(level)
                user_sport = UserSport.query.filter_by(user_id=user.id, sport_id=sport.id).first()
                if user_sport:
                    user_sport.level = level
                else:
                    new_user_sport = UserSport(user_id=user.id, sport_id=sport.id, level=level)
                    db.session.add(new_user_sport)

        db.session.commit()
        flash("Profil mis à jour avec succès.", "success")
        return redirect(url_for('profile.profile'))

    # Pre-fill the form with existing data
    form.username.data = user.username
    form.email.data = user.email
    form.first_name.data = user.first_name
    form.last_name.data = user.last_name
    form.country.data = user.country
    form.city.data = user.city
    form.address.data = user.address
    form.postal_code.data = user.postal_code
    form.sex.data = user.sex
    form.birth_date.data = user.birth_date
    form.phone.data = user.phone
    form.display_phone.data = user.display_phone
    form.display_email.data = user.display_email
    form.latitude.data = user.latitude
    form.longitude.data = user.longitude

    sports = Sport.query.all()
    return render_template('profile/edit_profile.html', user=user, form=form, sports=sports)

@profile_bp.route('/add_friend/<int:user_id>', methods=['POST'])
@login_required
def add_friend(user_id):
    user_to_add = User.query.get_or_404(user_id)
    if user_to_add == current_user:
        flash("Vous ne pouvez pas vous ajouter vous-même.", "danger")
        return redirect(url_for('profile.profile'))

    if current_user.is_friend(user_to_add):
        flash("Vous êtes déjà amis.", "info")
    else:
        current_user.friends.append(user_to_add)
        db.session.commit()
        flash(f"Vous êtes maintenant ami avec {user_to_add.username}.", "success")

    return redirect(url_for('profile.profile'))

@profile_bp.route('/friends', methods=['GET'])
@login_required
def list_friends():
    user = current_user
    friends = user.friends.all()
    return render_template('profile/friends_list.html', friends=friends, user=user)

@profile_bp.route('/photos/<int:user_id>', methods=['GET'])
@login_required
def photos(user_id):
    user = User.query.get_or_404(user_id)
    posts = Post.query.filter_by(user_id=user_id).filter(Post.image.isnot(None)).all()
    profile_images = [user.profile_image] if user.profile_image else []
    cover_images = [user.cover_image] if user.cover_image else []
    images = profile_images + cover_images + [post.image for post in posts]

    # Formulaire vide si nécessaire (pour utiliser hidden_tag())
    form = EmptyForm()

    if not images:
        flash("Aucune image disponible à afficher.", "info")
    
    # Passer l'instance de formulaire au template
    return render_template('profile/photos.html', user=user, images=images, form=form)

@profile_bp.route('/set_profile_photo/<string:photo_id>', methods=['GET', 'POST'])
@login_required
def set_profile_photo(photo_id):
    post = Post.query.get_or_404(photo_id)
    if post.user_id == current_user.id:
        current_user.profile_image = post.image
        db.session.commit()
        flash("Votre photo de profil a été mise à jour.", "success")
    return redirect(url_for('profile.photos', user_id=current_user.id))

@profile_bp.route('/set_cover_photo/<string:photo_id>', methods=['GET', 'POST'])
@login_required
def set_cover_photo(photo_id):
    post = Post.query.get_or_404(photo_id)
    if post.user_id == current_user.id:
        current_user.cover_image = post.image
        db.session.commit()
        flash("Votre photo de couverture a été mise à jour.", "success")
    return redirect(url_for('profile.photos', user_id=current_user.id))

@profile_bp.route('/complete_profile', methods=['GET', 'POST'])
@login_required
def complete_profile():
    form = CompleteProfileForm()
    # Populate the sports choices
    form.sports.choices = [(str(sport.id), sport.name) for sport in Sport.query.all()]
    form.levels.choices = [(str(i), f'{i} étoiles') for i in range(1, 6)]
    
    if form.validate_on_submit():
        # Update user's birth date and sex
        current_user.birth_date = form.birth_date.data
        current_user.sex = form.sex.data

        # Handle profile image upload
        if form.profile_image.data:
            profile_image_filename = save_image(form.profile_image.data, 'profiles')
            current_user.profile_image = profile_image_filename

        # Handle cover image upload
        if form.cover_image.data:
            cover_image_filename = save_image(form.cover_image.data, 'covers')
            current_user.cover_image = cover_image_filename

        # Save image positions and zoom levels
        current_user.profile_image_zoom = float(request.form.get('profile_image_zoom', 1.0))
        current_user.profile_image_pos_x = float(request.form.get('profile_image_pos_x', 0.0))
        current_user.profile_image_pos_y = float(request.form.get('profile_image_pos_y', 0.0))
        current_user.cover_image_zoom = float(request.form.get('cover_image_zoom', 1.0))
        current_user.cover_image_pos_x = float(request.form.get('cover_image_pos_x', 0.0))
        current_user.cover_image_pos_y = float(request.form.get('cover_image_pos_y', 0.0))

        # Clear existing sports
        UserSport.query.filter_by(user_id=current_user.id).delete()
        # Add selected sports and levels
        selected_sports = form.sports.data  # List of sport IDs as strings
        selected_levels = form.levels.data  # List of levels as strings
        for sport_id, level in zip(selected_sports, selected_levels):
            user_sport = UserSport(user_id=current_user.id, sport_id=int(sport_id), level=int(level))
            db.session.add(user_sport)

        db.session.commit()
        flash('Profil complété avec succès!', 'success')
        return redirect(url_for('profile.profile'))

    return render_template('profile/complete_profile.html', form=form)

def save_image(image_file, folder_name):
    filename = secure_filename(image_file.filename)
    path = os.path.join(current_app.root_path, 'static', 'uploads', folder_name, filename)
    image_file.save(path)
    return filename

@profile_bp.route('/friends')
@login_required
def friends():
    if current_user.friends.count() == 0:
        # Find users in the same city with similar sports
        similar_users = User.query.filter(
            User.city == current_user.city,
            User.id != current_user.id
        ).all()

        # Filter users based on shared sports and similar levels
        user_sports = {us.sport_id: us.level for us in current_user.sports}
        suggestions = []
        for user in similar_users:
            common_sports = []
            for us in user.sports:
                if us.sport_id in user_sports:
                    level_diff = abs(us.level - user_sports[us.sport_id])
                    if level_diff <= 1:  # Similar level
                        common_sports.append(us.sport.name)
            if common_sports:
                suggestions.append((user, common_sports))

        return render_template('profile/friends.html', suggestions=suggestions)
    else:
        friends = current_user.friends.all()
        return render_template('profile/friends.html', friends=friends)

@profile_bp.route('/add_photo', methods=['POST'])
@login_required
def add_photo():
    if 'photoUpload' in request.files:
        photos = request.files.getlist('photoUpload')
        for photo in photos:
            filename = secure_filename(photo.filename)
            photo.save(os.path.join(current_app.config['UPLOAD_FOLDER'], 'posts', filename))
            new_post = Post(
                user_id=current_user.id,
                image=filename,
                created_at=datetime.utcnow(),
                content='Photo ajoutée',  # Ajouter un contenu par défaut
                content_type='free',  # Exemple de type de contenu
                visibility='public'  # Exemple de visibilité par défaut
            )
            db.session.add(new_post)
        db.session.commit()
        flash("Photos ajoutées avec succès.", "success")
    else:
        flash("Aucune photo n'a été sélectionnée.", "danger")
    return redirect(url_for('profile.photos', user_id=current_user.id))

@profile_bp.route('/create_album', methods=['POST'])
@login_required
def create_album():
    album_name = request.form.get('albumName')
    # Logic to create an album can be added here (e.g., storing album info in the database)
    flash(f"Album '{album_name}' créé avec succès.", "success")
    return redirect(url_for('profile.photos', user_id=current_user.id))

def save_image(image_file, folder_name):
    filename = secure_filename(image_file.filename)
    path = os.path.join(current_app.root_path, 'static', 'uploads', folder_name, filename)
    image_file.save(path)
    return filename

@profile_bp.route('/search_users')
@login_required
def search_users():
    query = request.args.get('query', '')
    results = []
    if query:
        results = User.query.filter(
            (User.first_name.ilike(f'%{query}%')) | (User.last_name.ilike(f'%{query}%'))
        ).all()
    return render_template('profile/search_results.html', results=results, query=query)

@profile_bp.route('/view_profile/<int:user_id>')
@login_required
def view_profile(user_id):
    user = User.query.get_or_404(user_id)
    return render_template('profile/view_profile.html', user=user)
