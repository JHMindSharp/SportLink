from flask import Blueprint

# Define the blueprint for handling routes related to posts
# Définition du blueprint pour gérer les routes liées aux publications
posts_bp = Blueprint('posts', __name__)

# Import the routes for the 'posts' module to register them with the blueprint
# Importation des routes du module 'posts' pour les enregistrer avec le blueprint
from app.posts import routes
