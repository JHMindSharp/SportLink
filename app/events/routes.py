# app/events/routes.py

from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from app.events.form import EventForm
from app.extensions import db
from app.models import User

events_bp = Blueprint('events', __name__)

@events_bp.route('/organize', methods=['GET', 'POST'])
@login_required
def organize():
    """
    Permet de créer/rechercher une activité sportive 
    et d'afficher des partenaires potentiels.
    """
    form = EventForm()
    partners = []

    if form.validate_on_submit():
        # Exemple de matching
        # On suppose que user.sport/level existent ou qu'on matche autrement
        # Filtrage simplifié
        partners = User.query.filter(
            User.city == current_user.city
        ).all()
        
        if partners:
            flash("Recherche effectuée avec succès. Partenaires trouvés.", "success")
        else:
            flash("Aucun partenaire trouvé pour ces critères.", "warning")

    return render_template('events/organize.html', form=form, partners=partners)
