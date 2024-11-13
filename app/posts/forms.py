from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, FileField, SubmitField, SelectField
from wtforms.validators import DataRequired
from flask_wtf.file import FileAllowed

# Form class for creating a new post with various input types and validations
# Classe de formulaire pour créer une nouvelle publication avec différents types de saisie et validations
class CreatePostForm(FlaskForm):
    # Dropdown field to select the type of post (e.g., general or sports-related)
    # Champ déroulant pour sélectionner le type de publication (par exemple, générale ou sportive)
    content_type = SelectField('Type de Publication', choices=[('free', 'Publication Libre'), ('sport', 'Publication Sportive')], validators=[DataRequired()])
    
    # Text field for entering the title of the post
    # Champ de texte pour saisir le titre de la publication
    title = StringField('Titre')
    
    # Text field for entering the subtitle of the post
    # Champ de texte pour saisir le sous-titre de la publication
    subtitle = StringField('Sous-titre')
    
    # Text area for entering the main content of the post, required field
    # Zone de texte pour saisir le contenu principal de la publication, champ requis
    content = TextAreaField('Contenu', validators=[DataRequired()])
    
    # File upload field for adding an image, restricted to specific formats
    # Champ de téléchargement de fichier pour ajouter une image, limité à des formats spécifiques
    image = FileField('Ajouter une image', validators=[FileAllowed(['jpg', 'jpeg', 'png', 'gif'], 'Images uniquement!')])
    
    # File upload field for adding a video, restricted to specific formats
    # Champ de téléchargement de fichier pour ajouter une vidéo, limité à des formats spécifiques
    video = FileField('Ajouter une vidéo', validators=[FileAllowed(['mp4', 'avi', 'mov'], 'Vidéos uniquement!')])
    
    # File upload field for adding music, restricted to specific formats
    # Champ de téléchargement de fichier pour ajouter de la musique, limité à des formats spécifiques
    music = FileField('Ajouter de la musique', validators=[FileAllowed(['mp3', 'wav'], 'Fichiers audio uniquement!')])
    
    # Dropdown field to set the visibility of the post (public or private), required field
    # Champ déroulant pour définir la visibilité de la publication (publique ou privée), champ requis
    visibility = SelectField('Visibilité', choices=[('public', 'Public'), ('private', 'Privé')], validators=[DataRequired()])
    
    # Submit button to publish the post
    # Bouton de soumission pour publier la publication
    submit = SubmitField('Publier')
