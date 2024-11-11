from flask import Blueprint, render_template, request
from flask_login import login_required

events_bp = Blueprint('events', __name__)

@events_bp.route('/organize', methods=['GET', 'POST'])
@login_required
def organize():
    if request.method == 'POST':
        # Traitez le formulaire pour organiser une sortie sportive
        pass
    return render_template('events/organize.html')
