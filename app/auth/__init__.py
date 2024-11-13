from flask import Blueprint

# Creating the authentication blueprint for routing authentication-related views
# Création du blueprint d'authentification pour gérer les vues liées à l'authentification
auth_bp = Blueprint('auth', __name__)

# Importing routes for authentication to register them with the blueprint
# Importation des routes d'authentification pour les enregistrer avec le blueprint
from app.auth import routes
