from flask import Blueprint, render_template
from flask_login import login_required, current_user
from app.models import Notification  # Assurez-vous d'importer Notification

notifications_bp = Blueprint('notifications', __name__)

@notifications_bp.route('/list', methods=['GET'])
@login_required
def list_notifications():
    # Récupérer les notifications de l'utilisateur
    notifications = current_user.notifications.order_by(Notification.timestamp.desc()).all()
    return render_template('notifications/list.html', notifications=notifications)
