"""
app/events/forms.py

This module defines the forms used for creating or searching events in the SportLink application.
It leverages Flask-WTF for form handling and WTForms for validation.

Components:
- `EventForm`: A form for users to specify event details when searching for sports partners.
"""

from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, DateField, SelectField, SubmitField
from wtforms.validators import DataRequired

class EventForm(FlaskForm):
    """
    Form for searching for sports partners based on activity preferences.

    Fields:
    - sport: Dropdown for selecting the type of sport.
    - level: Dropdown for selecting the skill level.
    - distance: Integer input for the maximum distance in kilometers.
    - date: Date picker for specifying the event date.
    - submit: Submit button to trigger the search action.
    """
    sport = SelectField(
        'Sport', 
        choices=[
            ('running', 'Course à pied'), 
            ('cycling', 'Cyclisme')
        ], 
        validators=[DataRequired()]
    )
    level = SelectField(
        'Niveau', 
        choices=[
            ('beginner', 'Débutant'), 
            ('intermediate', 'Intermédiaire'), 
            ('advanced', 'Avancé')
        ], 
        validators=[DataRequired()]
    )
    distance = IntegerField(
        'Distance maximale (km)', 
        validators=[DataRequired()]
    )
    date = DateField(
        'Date', 
        format='%Y-%m-%d', 
        validators=[DataRequired()]
    )
    submit = SubmitField('Rechercher des Partenaires')
