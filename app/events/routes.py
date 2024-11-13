from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required
from app.events.form import EventForm
from app.models import User
from app.extensions import db

# Define the blueprint for event-related routes
# Définition du blueprint pour les routes liées aux événements
events_bp = Blueprint('events', __name__)

@events_bp.route('/organize', methods=['GET', 'POST'])
@login_required  # Ensures that only authenticated users can access this route
# S'assure que seuls les utilisateurs authentifiés peuvent accéder à cette route
def organize():
    # Instantiate the event form for the user to fill out
    # Instancie le formulaire d'événement à remplir par l'utilisateur
    form = EventForm()
    partners = []  # Initialize an empty list to store potential partners
    # Initialise une liste vide pour stocker les partenaires potentiels

    # Check if the form is submitted and valid
    # Vérifie si le formulaire est soumis et valide
    if form.validate_on_submit():
        # Query the database to find users matching the selected sport and level
        # Interroge la base de données pour trouver des utilisateurs correspondant au sport et au niveau sélectionnés
        partners = User.query.filter(
            User.sport == form.sport.data,
            User.level == form.level.data
        ).all()

        # Display a success message if partners are found
        # Affiche un message de succès si des partenaires sont trouvés
        if partners:
            flash("Recherche effectuée avec succès. Partenaires trouvés.", "success")
        else:
            # Display a warning message if no partners are found
            # Affiche un message d'avertissement si aucun partenaire n'est trouvé
            flash("Aucun partenaire trouvé pour ces critères.", "warning")

    # Render the event organization template with the form and list of partners
    # Rendu du modèle d'organisation d'événements avec le formulaire et la liste des partenaires
    return render_template('events/organize.html', form=form, partners=partners)
