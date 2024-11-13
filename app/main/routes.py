import os
from flask import Blueprint, render_template, jsonify, send_from_directory, current_app, redirect, url_for
from flask_login import current_user
from app.extensions import db
from app.auth.forms import RegistrationForm, LoginForm

# Define the blueprint for main application routes
# Définition du blueprint pour les routes principales de l'application
main_bp = Blueprint('main', __name__)

@main_bp.route('/')
# Route for the home page, redirects authenticated users and displays forms for new users
# Route pour la page d'accueil, redirige les utilisateurs authentifiés et affiche les formulaires pour les nouveaux utilisateurs
def index():
    if current_user.is_authenticated:
        # Redirect to the profile page if the user is already logged in
        # Redirige vers la page de profil si l'utilisateur est déjà connecté
        return redirect(url_for('profile.profile'))
    
    # Create registration and login forms for display on the home page
    # Crée les formulaires d'inscription et de connexion à afficher sur la page d'accueil
    register_form = RegistrationForm()
    login_form = LoginForm()
    return render_template('home.html', register_form=register_form, login_form=login_form)

@main_bp.app_errorhandler(404)
# Custom error handler for 404 (Not Found) errors
# Gestionnaire d'erreurs personnalisé pour les erreurs 404 (non trouvé)
def not_found_error(error):
    # Render a 404 error page with forms for user interaction
    # Affiche une page d'erreur 404 avec des formulaires pour l'interaction utilisateur
    register_form = RegistrationForm()
    login_form = LoginForm()
    return render_template('404.html', register_form=register_form, login_form=login_form), 404

@main_bp.app_errorhandler(500)
# Custom error handler for 500 (Internal Server Error)
# Gestionnaire d'erreurs personnalisé pour les erreurs 500 (erreur interne du serveur)
def internal_error(error):
    # Roll back the database session to ensure data integrity
    # Annule la session de la base de données pour assurer l'intégrité des données
    db.session.rollback()
    # Render a 500 error page with forms for user interaction
    # Affiche une page d'erreur 500 avec des formulaires pour l'interaction utilisateur
    register_form = RegistrationForm()
    login_form = LoginForm()
    return render_template('500.html', register_form=register_form, login_form=login_form), 500

@main_bp.route('/uploads/<path:filename>')
# Route for serving uploaded files from a directory
# Route pour servir des fichiers téléchargés à partir d'un répertoire
def uploaded_file(filename):
    # Send the requested file from the UPLOAD_FOLDER directory
    # Envoie le fichier demandé depuis le répertoire UPLOAD_FOLDER
    return send_from_directory(current_app.config['UPLOAD_FOLDER'], filename)

@main_bp.route('/privacy_policy')
# Route for displaying the privacy policy page
# Route pour afficher la page de politique de confidentialité
def privacy_policy():
    return render_template('main/privacy_policy.html')
