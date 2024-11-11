from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, FileField, SubmitField, SelectField
from wtforms.validators import DataRequired
from flask_wtf.file import FileAllowed

class CreatePostForm(FlaskForm):
    content_type = SelectField('Type de Publication', choices=[('free', 'Publication Libre'), ('sport', 'Publication Sportive')], validators=[DataRequired()])
    title = StringField('Titre')
    subtitle = StringField('Sous-titre')
    content = TextAreaField('Contenu', validators=[DataRequired()])
    image = FileField('Ajouter une image', validators=[FileAllowed(['jpg', 'jpeg', 'png', 'gif'], 'Images uniquement!')])
    video = FileField('Ajouter une vidéo', validators=[FileAllowed(['mp4', 'avi', 'mov'], 'Vidéos uniquement!')])
    music = FileField('Ajouter de la musique', validators=[FileAllowed(['mp3', 'wav'], 'Fichiers audio uniquement!')])
    visibility = SelectField('Visibilité', choices=[('public', 'Public'), ('private', 'Privé')], validators=[DataRequired()])
    submit = SubmitField('Publier')
