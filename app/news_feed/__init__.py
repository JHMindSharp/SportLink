from flask import Blueprint

# Define the blueprint for the 'news_feed' module, which handles routes related to the news feed
# Définition du blueprint pour le module 'news_feed', qui gère les routes liées au fil d'actualité
news_feed_bp = Blueprint('news_feed', __name__)

# Import the routes for the 'news_feed' module to register them with the blueprint
# Importation des routes du module 'news_feed' pour les enregistrer avec le blueprint
from app.news_feed import routes
