from flask import Blueprint

# Define the blueprint for the 'messages' module, which will handle message-related routes and views
# Définition du blueprint pour le module 'messages', qui gérera les routes et vues liées aux messages
messages_bp = Blueprint('messages', __name__)

# Import the routes for the 'messages' module to register them with the blueprint
# Importation des routes du module 'messages' pour les enregistrer avec le blueprint
from app.messages import routes
