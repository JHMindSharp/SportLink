from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, DateField, SelectField, SubmitField
from wtforms.validators import DataRequired

class EventForm(FlaskForm):
    sport = SelectField('Sport', choices=[('running', 'Course à pied'), ('cycling', 'Cyclisme')], validators=[DataRequired()])
    level = SelectField('Niveau', choices=[('beginner', 'Débutant'), ('intermediate', 'Intermédiaire'), ('advanced', 'Avancé')], validators=[DataRequired()])
    distance = IntegerField('Distance maximale (km)', validators=[DataRequired()])
    date = DateField('Date', format='%Y-%m-%d', validators=[DataRequired()])
    submit = SubmitField('Rechercher des Partenaires')
