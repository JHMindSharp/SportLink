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

# Define the blueprint for handling profile-related routes
# Définition du blueprint pour gérer les routes liées au profil
profile_bp = Blueprint('profile', __name__)

# Define an empty form for general use in templates
# Définir un formulaire vide pour une utilisation générale dans les modèles
class EmptyForm(FlaskForm):
    pass

@profile_bp.route('/settings', methods=['GET', 'POST'])
@login_required  # Ensures that only authenticated users can access the settings page
# S'assure que seuls les utilisateurs authentifiés peuvent accéder à la page des paramètres
def settings():
    # Instantiate forms for changing email, password, and deleting account
    # Instancie les formulaires pour changer l'email, le mot de passe et supprimer le compte
    change_email_form = ChangeEmailForm()
    change_password_form = ChangePasswordForm()
    delete_account_form = DeleteAccountForm()
    return render_template('profile/settings.html', change_email_form=change_email_form, change_password_form=change_password_form, delete_account_form=delete_account_form)

@profile_bp.route('/change_email', methods=['POST'])
@login_required
# Route for changing the user's email
# Route pour changer l'email de l'utilisateur
def change_email():
    form = ChangeEmailForm()
    if form.validate_on_submit():
        # Update the user's email and commit the changes to the database
        # Met à jour l'email de l'utilisateur et enregistre les changements dans la base de données
        current_user.email = form.email.data
        db.session.commit()
        flash("Votre adresse email a été mise à jour.", "success")
    else:
        flash("Erreur lors de la mise à jour de l'email.", "danger")
    return redirect(url_for('profile.settings'))

@profile_bp.route('/change_password', methods=['POST'])
@login_required
# Route for changing the user's password
# Route pour changer le mot de passe de l'utilisateur
def change_password():
    form = ChangePasswordForm()
    if form.validate_on_submit():
        # Set the new password and commit the changes to the database
        # Met à jour le mot de passe et enregistre les changements dans la base de données
        current_user.set_password(form.new_password.data)
        db.session.commit()
        flash("Votre mot de passe a été mis à jour. Veuillez vous reconnecter.", "success")
        logout_user()  # Log out the user after password change
        # Déconnecte l'utilisateur après la mise à jour du mot de passe
        return redirect(url_for('auth.login'))
    else:
        flash("Erreur lors de la mise à jour du mot de passe.", "danger")
    return redirect(url_for('profile.settings'))

@profile_bp.route('/delete_account', methods=['POST'])
@login_required
# Route for deleting the user's account
# Route pour supprimer le compte de l'utilisateur
def delete_account():
    form = DeleteAccountForm()
    if form.validate_on_submit():
        # Get the current user object and delete it from the database
        # Récupère l'objet utilisateur actuel et le supprime de la base de données
        user = current_user._get_current_object()
        if isinstance(user, User):  # Check that the user is a User instance
            db.session.delete(user)
            db.session.commit()
            logout_user()  # Log out after deleting the account
            # Déconnecte l'utilisateur après la suppression du compte
            flash("Votre compte a été supprimé.", "success")
            return redirect(url_for('main.index'))
        else:
            flash("Erreur lors de la suppression du compte.", "danger")
    else:
        flash("Erreur lors de la validation du formulaire.", "danger")
    return redirect(url_for('profile.settings'))

@profile_bp.route('/profile', methods=['GET'])
@login_required
# Route for displaying the user's profile
# Route pour afficher le profil de l'utilisateur
def profile():
    user = current_user
    # Get the average rating and the total number of ratings received
    # Récupère la note moyenne et le nombre total de notes reçues
    average_rating = user.average_rating
    total_ratings = user.ratings_received.count()
    # Get the user's posts ordered by creation date (newest first)
    # Récupère les publications de l'utilisateur triées par date de création (les plus récentes en premier)
    posts = user.posts.order_by(Post.created_at.desc()).all()
    sports = Sport.query.all()  # Get all sports for display
    # Récupère tous les sports pour l'affichage
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
# Route for editing the user's profile
# Route pour modifier le profil de l'utilisateur
def edit_profile():
    user = current_user
    form = EditProfileForm()

    if form.validate_on_submit():
        # Update user fields with form data and save images if provided
        # Met à jour les champs de l'utilisateur avec les données du formulaire et enregistre les images si fournies
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

        # Save profile image if provided
        # Enregistre l'image de profil si fournie
        if form.profile_image.data:
            profile_image = form.profile_image.data
            filename = secure_filename(profile_image.filename)
            profile_image_path = os.path.join(current_app.config['UPLOAD_FOLDER'], 'profiles', filename)
            profile_image.save(profile_image_path)
            user.profile_image = filename

        # Save cover image if provided
        # Enregistre l'image de couverture si fournie
        if form.cover_image.data:
            cover_image = form.cover_image.data
            filename = secure_filename(cover_image.filename)
            cover_image_path = os.path.join(current_app.config['UPLOAD_FOLDER'], 'covers', filename)
            cover_image.save(cover_image_path)
            user.cover_image = filename

        # Update or add sports and levels for the user
        # Met à jour ou ajoute les sports et niveaux pour l'utilisateur
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

        db.session.commit()  # Commit changes to the database
        # Enregistre les changements dans la base de données
        flash("Profil mis à jour avec succès.", "success")
        return redirect(url_for('profile.profile'))

    # Pre-fill the form with existing user data for editing
    # Pré-remplit le formulaire avec les données existantes de l'utilisateur pour modification
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

    sports = Sport.query.all()  # Get all sports for display
    # Récupère tous les sports pour l'affichage
    return render_template('profile/edit_profile.html', user=user, form=form, sports=sports)

@profile_bp.route('/add_friend/<int:user_id>', methods=['POST'])
@login_required
# Route for adding a friend
# Route pour ajouter un ami
def add_friend(user_id):
    user_to_add = User.query.get_or_404(user_id)  # Get the user to be added or return a 404 if not found
    # Récupère l'utilisateur à ajouter ou renvoie un 404 s'il n'est pas trouvé
    if user_to_add == current_user:
        flash("Vous ne pouvez pas vous ajouter vous-même.", "danger")
        return redirect(url_for('profile.profile'))

    if current_user.is_friend(user_to_add):  # Check if they are already friends
        # Vérifie s'ils sont déjà amis
        flash("Vous êtes déjà amis.", "info")
    else:
        current_user.friends.append(user_to_add)  # Add the user to the friends list
        # Ajoute l'utilisateur à la liste d'amis
        db.session.commit()
        flash(f"Vous êtes maintenant ami avec {user_to_add.username}.", "success")

    return redirect(url_for('profile.profile'))

@profile_bp.route('/friends', methods=['GET'])
@login_required
# Route for listing the user's friends
# Route pour lister les amis de l'utilisateur
def list_friends():
    user = current_user
    friends = user.friends.all()  # Get all friends of the current user
    # Récupère tous les amis de l'utilisateur actuel
    return render_template('profile/friends_list.html', friends=friends, user=user)

@profile_bp.route('/photos/<int:user_id>', methods=['GET'])
@login_required
# Route for displaying a user's photos
# Route pour afficher les photos d'un utilisateur
def photos(user_id):
    user = User.query.get_or_404(user_id)
    # Get all posts by the user that include an image
    # Récupère toutes les publications de l'utilisateur contenant une image
    posts = Post.query.filter_by(user_id=user_id).filter(Post.image.isnot(None)).all()
    profile_images = [user.profile_image] if user.profile_image else []
    cover_images = [user.cover_image] if user.cover_image else []
    images = profile_images + cover_images + [post.image for post in posts]

    # Use an empty form for additional functionalities in the template
    # Utilise un formulaire vide pour des fonctionnalités supplémentaires dans le modèle
    form = EmptyForm()

    if not images:
        flash("Aucune image disponible à afficher.", "info")
    
    # Pass the form instance to the template
    # Passe l'instance de formulaire au modèle
    return render_template('profile/photos.html', user=user, images=images, form=form)

@profile_bp.route('/set_profile_photo/<string:photo_id>', methods=['GET', 'POST'])
@login_required
# Route for setting a photo as the user's profile picture
# Route pour définir une photo comme image de profil de l'utilisateur
def set_profile_photo(photo_id):
    post = Post.query.get_or_404(photo_id)
    if post.user_id == current_user.id:
        current_user.profile_image = post.image
        db.session.commit()
        flash("Votre photo de profil a été mise à jour.", "success")
    return redirect(url_for('profile.photos', user_id=current_user.id))

@profile_bp.route('/set_cover_photo/<string:photo_id>', methods=['GET', 'POST'])
@login_required
# Route for setting a photo as the user's cover picture
# Route pour définir une photo comme image de couverture de l'utilisateur
def set_cover_photo(photo_id):
    post = Post.query.get_or_404(photo_id)
    if post.user_id == current_user.id:
        current_user.cover_image = post.image
        db.session.commit()
        flash("Votre photo de couverture a été mise à jour.", "success")
    return redirect(url_for('profile.photos', user_id=current_user.id))

@profile_bp.route('/complete_profile', methods=['GET', 'POST'])
@login_required
# Route for completing the user's profile with additional details
# Route pour compléter le profil de l'utilisateur avec des détails supplémentaires
def complete_profile():
    form = CompleteProfileForm()
    # Populate the sports choices
    # Remplit les choix de sports
    form.sports.choices = [(str(sport.id), sport.name) for sport in Sport.query.all()]
    form.levels.choices = [(str(i), f'{i} étoiles') for i in range(1, 6)]
    
    if form.validate_on_submit():
        # Update user's birth date and sex
        # Met à jour la date de naissance et le sexe de l'utilisateur
        current_user.birth_date = form.birth_date.data
        current_user.sex = form.sex.data

        # Handle profile image upload
        # Gestion de l'upload de l'image de profil
        if form.profile_image.data:
            profile_image_filename = save_image(form.profile_image.data, 'profiles')
            current_user.profile_image = profile_image_filename

        # Handle cover image upload
        # Gestion de l'upload de l'image de couverture
        if form.cover_image.data:
            cover_image_filename = save_image(form.cover_image.data, 'covers')
            current_user.cover_image = cover_image_filename

        # Save image positions and zoom levels
        # Enregistre les positions et niveaux de zoom des images
        current_user.profile_image_zoom = float(request.form.get('profile_image_zoom', 1.0))
        current_user.profile_image_pos_x = float(request.form.get('profile_image_pos_x', 0.0))
        current_user.profile_image_pos_y = float(request.form.get('profile_image_pos_y', 0.0))
        current_user.cover_image_zoom = float(request.form.get('cover_image_zoom', 1.0))
        current_user.cover_image_pos_x = float(request.form.get('cover_image_pos_x', 0.0))
        current_user.cover_image_pos_y = float(request.form.get('cover_image_pos_y', 0.0))

        # Clear existing sports and add selected ones with levels
        # Supprime les sports existants et ajoute ceux sélectionnés avec les niveaux
        UserSport.query.filter_by(user_id=current_user.id).delete()
        selected_sports = form.sports.data  # List of sport IDs as strings
        selected_levels = form.levels.data  # List of levels as strings
        for sport_id, level in zip(selected_sports, selected_levels):
            user_sport = UserSport(user_id=current_user.id, sport_id=int(sport_id), level=int(level))
            db.session.add(user_sport)

        db.session.commit()
        flash('Profil complété avec succès!', 'success')
        return redirect(url_for('profile.profile'))

    return render_template('profile/complete_profile.html', form=form)

# Utility function for saving uploaded images to a specified folder
# Fonction utilitaire pour enregistrer les images téléchargées dans un dossier spécifié
def save_image(image_file, folder_name):
    filename = secure_filename(image_file.filename)
    path = os.path.join(current_app.root_path, 'static', 'uploads', folder_name, filename)
    image_file.save(path)
    return filename

@profile_bp.route('/search_users')
@login_required
# Route for searching users based on a query
# Route pour rechercher des utilisateurs en fonction d'une requête
def search_users():
    query = request.args.get('query', '')
    results = []
    if query:
        # Search users by matching first or last name
        # Recherche des utilisateurs en fonction du prénom ou du nom
        results = User.query.filter(
            (User.first_name.ilike(f'%{query}%')) | (User.last_name.ilike(f'%{query}%'))
        ).all()
    return render_template('profile/search_results.html', results=results, query=query)

@profile_bp.route('/view_profile/<int:user_id>')
@login_required
# Route for viewing another user's profile
# Route pour voir le profil d'un autre utilisateur
def view_profile(user_id):
    user = User.query.get_or_404(user_id)
    return render_template('profile/view_profile.html', user=user)
