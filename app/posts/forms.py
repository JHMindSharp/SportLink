"""
app/posts/forms.py

This module defines forms related to post creation in the SportLink application.
It uses Flask-WTF for form handling and WTForms for validation.

Components:
- `CreatePostForm`: Form to create a post with options for content type, title, multimedia, and visibility.
"""

from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, FileField, SubmitField, SelectField
from wtforms.validators import DataRequired
from flask_wtf.file import FileAllowed

class CreatePostForm(FlaskForm):
    """
    Form for creating a new post.

    Fields:
    - `content_type`: Dropdown to select the type of post (free or sport-related).
    - `title`: Optional text input for the post's title.
    - `subtitle`: Optional text input for the post's subtitle.
    - `content`: Text area for the main content of the post (required).
    - `image`: File upload field for an image (optional, accepts JPG, PNG, GIF).
    - `video`: File upload field for a video (optional, accepts MP4, AVI, MOV).
    - `music`: File upload field for an audio file (optional, accepts MP3, WAV).
    - `visibility`: Dropdown to set the post's visibility (public or private).
    - `submit`: Submit button to publish the post.
    """
    content_type = SelectField(
        'Type de Publication', 
        choices=[
            ('free', 'Publication Libre'), 
            ('sport', 'Publication Sportive')
        ], 
        validators=[DataRequired()]
    )
    title = StringField('Titre')
    subtitle = StringField('Sous-titre')
    content = TextAreaField(
        'Contenu', 
        validators=[DataRequired()]
    )
    image = FileField(
        'Ajouter une image', 
        validators=[FileAllowed(['jpg', 'jpeg', 'png', 'gif'], 'Images uniquement!')]
    )
    video = FileField(
        'Ajouter une vidéo', 
        validators=[FileAllowed(['mp4', 'avi', 'mov'], 'Vidéos uniquement!')]
    )
    music = FileField(
        'Ajouter de la musique', 
        validators=[FileAllowed(['mp3', 'wav'], 'Fichiers audio uniquement!')]
    )
    visibility = SelectField(
        'Visibilité', 
        choices=[
            ('public', 'Public'), 
            ('private', 'Privé')
        ], 
        validators=[DataRequired()]
    )
    submit = SubmitField('Publier')
