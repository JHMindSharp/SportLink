from flask import Blueprint

# Define the blueprint for handling profile-related routes
# Définition du blueprint pour gérer les routes liées au profil
profile_bp = Blueprint('profile', __name__)

# Import the routes for the 'profile' module to register them with the blueprint
# Importation des routes du module 'profile' pour les enregistrer avec le blueprint
from app.profile import routes
