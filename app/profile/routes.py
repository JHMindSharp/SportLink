# app/profile/routes.py

from flask import Blueprint, request, render_template, redirect, url_for, flash, abort, jsonify, current_app
from flask_login import login_required, current_user, logout_user
from datetime import datetime
import os
import uuid
from werkzeug.utils import secure_filename

from app.extensions import db
from app.models import User, Sport, Rating, Post, UserSport
from app.profile.forms import (
    EditProfileForm,
    ChangeEmailForm,
    ChangePasswordForm,
    DeleteAccountForm,
    CompleteProfileForm,
    ChangePhotoForm,
)
from app.auth.forms import RegistrationForm, LoginForm
from flask_wtf import FlaskForm

profile_bp = Blueprint('profile', __name__)

class EmptyForm(FlaskForm):
    # Ce formulaire ne contient que le token caché
    pass

def save_image(image_file, folder_name, user_id):
    filename = secure_filename(image_file.filename)
    unique_prefix = str(uuid.uuid4())
    final_filename = f"{unique_prefix}_{filename}"

    user_folder = os.path.join(current_app.config['UPLOAD_FOLDER'], folder_name, str(user_id))
    os.makedirs(user_folder, exist_ok=True)

    file_path = os.path.join(user_folder, final_filename)
    image_file.save(file_path)
    return f"{folder_name}/{user_id}/{final_filename}"

@profile_bp.route('/settings', methods=['GET', 'POST'])
@login_required
def settings():
    change_email_form = ChangeEmailForm()
    change_password_form = ChangePasswordForm()
    delete_account_form = DeleteAccountForm()
    return render_template(
        'profile/settings.html',
        change_email_form=change_email_form,
        change_password_form=change_password_form,
        delete_account_form=delete_account_form
    )

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
        logout_user()
        return redirect(url_for('auth.login'))
    else:
        flash("Erreur lors de la mise à jour du mot de passe.", "danger")
    return redirect(url_for('profile.settings'))

@profile_bp.route('/delete_account', methods=['POST'])
@login_required
def delete_account():
    form = DeleteAccountForm()
    if form.validate_on_submit():
        user = current_user._get_current_object()
        if isinstance(user, User):
            db.session.delete(user)
            db.session.commit()
            logout_user()
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
    """Affiche la page de profil du current_user (ou param user_id si voulu)."""
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

@profile_bp.route('/profile/<int:user_id>', methods=['GET'])
@login_required
def profile_other(user_id):
    """Affiche le profil d'un autre utilisateur, si on veut user_id différent."""
    user = User.query.get_or_404(user_id)
    posts = user.posts.order_by(Post.created_at.desc()).all()
    return render_template('profile/profile.html', user=user, posts=posts)

@profile_bp.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    user = current_user
    form = EditProfileForm()

    if form.validate_on_submit():
        user.first_name = form.first_name.data
        user.last_name = form.last_name.data
        user.email = form.email.data
        user.city = form.city.data
        user.country = form.country.data
        user.phone = form.phone.data
        user.display_phone = form.display_phone.data
        user.display_email = form.display_email.data

        # S’il y a un fichier uploadé, on appelle save_image()
        if form.profile_image.data:
            user.profile_image = save_image(form.profile_image.data, 'profiles', user.id)
        # Sinon, on NE change pas user.profile_image.
        # S’il était None, il le reste.

        if form.cover_image.data:
            user.cover_image = save_image(form.cover_image.data, 'covers', user.id)

        db.session.commit()
        flash("Profil mis à jour avec succès.", "success")
        return redirect(url_for('profile.profile'))

    # Pré-remplir
    form.first_name.data = user.first_name
    form.last_name.data = user.last_name
    form.email.data = user.email
    form.city.data = user.city
    form.country.data = user.country
    form.phone.data = user.phone
    form.display_phone.data = user.display_phone
    form.display_email.data = user.display_email

    return render_template('profile/edit_profile.html', form=form)
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
        flash(f"Vous êtes maintenant ami avec {user_to_add.first_name}.", "success")

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
    posts = Post.query.filter_by(user_id=user.id).filter(Post.image.isnot(None)).all()
    profile_images = [user.profile_image] if user.profile_image else []
    cover_images = [user.cover_image] if user.cover_image else []
    images = profile_images + cover_images + [p.image for p in posts if p.image]

    form = EmptyForm()

    if not images:
        flash("Aucune image disponible à afficher.", "info")

    return render_template('profile/photos.html', user=user, images=images, form=form)

@profile_bp.route('/complete_profile', methods=['GET', 'POST'])
@login_required
def complete_profile():
    """Exemple de formulaire WTForms plus poussé, si voulu."""
    form = CompleteProfileForm()
    form.sports.choices = [(str(s.id), s.name) for s in Sport.query.all()]
    form.levels.choices = [(str(i), f'{i} étoiles') for i in range(1, 6)]

    if form.validate_on_submit():
        current_user.birth_date = form.birth_date.data
        current_user.sex = form.sex.data

        if form.profile_image.data:
            profile_image_filename = save_image(form.profile_image.data, 'profiles', current_user.id)
            current_user.profile_image = profile_image_filename
        if form.cover_image.data:
            cover_image_filename = save_image(form.cover_image.data, 'covers', current_user.id)
            current_user.cover_image = cover_image_filename

        UserSport.query.filter_by(user_id=current_user.id).delete()
        selected_sports = form.sports.data
        selected_levels = form.levels.data
        for sport_id, level in zip(selected_sports, selected_levels):
            user_sport = UserSport(user_id=current_user.id, sport_id=int(sport_id), level=int(level))
            db.session.add(user_sport)

        current_user.profile_completed = True
        db.session.commit()
        flash('Profil complété avec succès!', 'success')
        return redirect(url_for('profile.profile'))

    return render_template('profile/complete_profile.html', form=form)

@profile_bp.route('/search_users', methods=['GET'])
@login_required
def search_users():
    query = request.args.get('query', '').strip()
    suggestions = []
    results = []

    form = EmptyForm()

    if query:
        results = User.query.filter(
            (User.first_name.ilike(f'%{query}%')) | (User.last_name.ilike(f'%{query}%'))
        ).all()
    else:
        # Quelques suggestions. On peut filtrer par ville, etc.
        suggestions = User.query.filter(
            User.id != current_user.id
        ).limit(10).all()

    return render_template('profile/search_results.html', results=results, suggestions=suggestions, query=query, form=form)

@profile_bp.route('/add_contact/<int:user_id>', methods=['POST'])
@login_required
def add_contact(user_id):
    form = EmptyForm()
    if not form.validate_on_submit():
        flash("Erreur de soumission. Merci de réessayer.", "danger")
        return redirect(url_for('profile.list_contacts'))

    user_to_add = User.query.get_or_404(user_id)
    if user_to_add == current_user:
        flash("Vous ne pouvez pas vous ajouter vous-même.", "danger")
        return redirect(url_for('profile.list_contacts'))

    if current_user.is_friend(user_to_add):
        flash("Cette personne est déjà dans vos contacts.", "info")
    else:
        current_user.friends.append(user_to_add)
        db.session.commit()
        flash(f"{user_to_add.first_name} {user_to_add.last_name} a été ajouté à vos contacts.", "success")

    return redirect(url_for('profile.list_contacts'))

@profile_bp.route('/contacts', methods=['GET'])
@login_required
def list_contacts():
    contacts = current_user.friends.all()
    return render_template('profile/contacts.html', contacts=contacts)

@profile_bp.route('/remove_contact/<int:user_id>', methods=['POST'])
@login_required
def remove_contact(user_id):
    user_to_remove = User.query.get_or_404(user_id)
    if current_user.is_friend(user_to_remove):
        current_user.friends.remove(user_to_remove)
        db.session.commit()
        flash(f"{user_to_remove.first_name} {user_to_remove.last_name} a été retiré de vos contacts.", "success")
    else:
        flash("Cette personne n'est pas dans vos contacts.", "info")

    return redirect(url_for('profile.list_contacts'))

UPLOAD_FOLDER = 'app/static/uploads'
COVER_FOLDER = os.path.join(UPLOAD_FOLDER, 'covers')
PROFILE_FOLDER = os.path.join(UPLOAD_FOLDER, 'profiles')

# Autoriser uniquement certains types de fichiers
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@profile_bp.route('/change_photo/<type>', methods=['GET', 'POST'])
@login_required
def change_photo(type):
    # Vérification du type
    if type not in ['cover', 'profile']:
        abort(404)  # Renvoie une erreur 404 si le type est invalide

    form = ChangePhotoForm()

    if form.validate_on_submit():
        # Gestion du fichier téléchargé
        if 'file' not in request.files:
            flash('Aucun fichier sélectionné.', 'danger')
            return redirect(request.url)

        file = request.files['file']
        if file.filename == '':
            flash('Aucun fichier sélectionné.', 'danger')
            return redirect(request.url)

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            save_folder = COVER_FOLDER if type == 'cover' else PROFILE_FOLDER

            os.makedirs(save_folder, exist_ok=True)
            filepath = os.path.join(save_folder, filename)
            file.save(filepath)

            # Mise à jour de l'utilisateur
            if type == 'cover':
                current_user.cover_image = filename
            elif type == 'profile':
                current_user.profile_image = filename

            db.session.commit()
            flash('Photo mise à jour avec succès.', 'success')
            return redirect(url_for('profile.profile'))

        flash('Fichier non autorisé.', 'danger')
        return redirect(request.url)

    # Retourne toujours le template si aucune condition n'est remplie
    return render_template('profile/change_photo.html', form=form, photo_type=type)
