from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, DateField, SelectField, SubmitField
from wtforms.validators import DataRequired

# Form class for searching event partners with various filters
# Classe de formulaire pour rechercher des partenaires d'événements avec divers filtres
class EventForm(FlaskForm):
    # Dropdown field for selecting the type of sport, required for filtering events
    # Champ déroulant pour sélectionner le type de sport, requis pour filtrer les événements
    sport = SelectField('Sport', choices=[('running', 'Course à pied'), ('cycling', 'Cyclisme')], validators=[DataRequired()])
    
    # Dropdown field for selecting the user's skill level, required for matching with appropriate partners
    # Champ déroulant pour sélectionner le niveau de compétence de l'utilisateur, requis pour trouver des partenaires appropriés
    level = SelectField('Niveau', choices=[('beginner', 'Débutant'), ('intermediate', 'Intermédiaire'), ('advanced', 'Avancé')], validators=[DataRequired()])
    
    # Field for entering the maximum distance for the event in kilometers, required for specifying event scope
    # Champ pour entrer la distance maximale pour l'événement en kilomètres, requis pour spécifier la portée de l'événement
    distance = IntegerField('Distance maximale (km)', validators=[DataRequired()])
    
    # Field for specifying the date of the event, formatted as YYYY-MM-DD, required for scheduling
    # Champ pour spécifier la date de l'événement, formaté en AAAA-MM-JJ, requis pour la planification
    date = DateField('Date', format='%Y-%m-%d', validators=[DataRequired()])
    
    # Submit button for submitting the form to search for partners
    # Bouton de soumission pour envoyer le formulaire et rechercher des partenaires
    submit = SubmitField('Rechercher des Partenaires')
