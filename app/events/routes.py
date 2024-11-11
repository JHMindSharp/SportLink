from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required
from app.events.form import EventForm
from app.models import User  # Assurez-vous que la classe User est bien importée
from app.extensions import db  # Si des requêtes supplémentaires nécessitent la base de données

events_bp = Blueprint('events', __name__)

@events_bp.route('/organize', methods=['GET', 'POST'])
@login_required
def organize():
    form = EventForm()
    partners = []  # Liste des partenaires potentiels

    if form.validate_on_submit():
        # Logique pour trouver les partenaires basés sur les critères du formulaire
        partners = User.query.filter(
            User.sport == form.sport.data,
            User.level == form.level.data
        ).all()

        if partners:
            flash("Recherche effectuée avec succès. Partenaires trouvés.", "success")
        else:
            flash("Aucun partenaire trouvé pour ces critères.", "warning")

    return render_template('events/organize.html', form=form, partners=partners)
