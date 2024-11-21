"""
app/events/routes.py

This module handles the routes related to event organization in the SportLink application.
It provides functionalities for users to organize or search for sports partners based on their preferences.

Components:
- `organize`: Route for creating an event and searching for potential partners.
"""

from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required
from app.events.form import EventForm
from app.models import User
from app.extensions import db

# Define the blueprint for event-related routes
events_bp = Blueprint('events', __name__)

@events_bp.route('/organize', methods=['GET', 'POST'])
@login_required
def organize():
    """
    Allows users to organize events and search for potential sports partners.

    - Uses `EventForm` to gather user preferences (sport, level, distance, date).
    - Filters users from the database who match the specified criteria.
    - Displays matching partners or an appropriate message if none are found.

    Methods:
    - GET: Renders the event organization form.
    - POST: Processes the form submission and performs the partner search.

    Returns:
    - Renders `events/organize.html` with the form and list of partners.
    """
    form = EventForm()  # Initialize the form
    partners = []  # List to hold the search results

    # Handle form submission
    if form.validate_on_submit():
        # Query the database for matching partners
        partners = User.query.filter(
            User.sport == form.sport.data,
            User.level == form.level.data
        ).all()

        # Flash messages based on the search results
        if partners:
            flash("Recherche effectuée avec succès. Partenaires trouvés.", "success")
        else:
            flash("Aucun partenaire trouvé pour ces critères.", "warning")

    # Render the event organization template with the form and results
    return render_template('events/organize.html', form=form, partners=partners)
