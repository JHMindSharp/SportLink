from flask import Blueprint, render_template
from flask_login import login_required, current_user
from app.models import Notification


# Define the blueprint for handling notification-related routes
# Définition du blueprint pour gérer les routes liées aux notifications
notifications_bp = Blueprint('notifications', __name__)

@notifications_bp.route('/list', methods=['GET'])
@login_required  # Ensure that only authenticated users can access the notification list
# S'assure que seuls les utilisateurs authentifiés peuvent accéder à la liste des notifications
def list_notifications():
    # Retrieve the current user's notifications, ordered by timestamp from newest to oldest
    # Récupère les notifications de l'utilisateur actuel, triées par horodatage de la plus récente à la plus ancienne
    notifications = current_user.notifications.order_by(Notification.timestamp.desc()).all()
    
    # Render the template for displaying the list of notifications
    # Affiche le modèle pour présenter la liste des notifications
    return render_template('notifications/list.html', notifications=notifications)
