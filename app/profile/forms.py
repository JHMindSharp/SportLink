from flask_wtf import FlaskForm
from wtforms import (
    StringField, PasswordField, SubmitField, BooleanField, FileField,
    SelectField, DateField, HiddenField, TelField, FloatField, SelectMultipleField
)
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError, Optional
from flask_wtf.file import FileAllowed, FileField
from app.models import User
from wtforms_sqlalchemy.fields import QuerySelectMultipleField
from wtforms.widgets import ListWidget, CheckboxInput

# Form class for changing the user's email address with validation
# Classe de formulaire pour changer l'adresse email de l'utilisateur avec validation
class ChangeEmailForm(FlaskForm):
    # Field for the new email address with validation for format and presence
    # Champ pour la nouvelle adresse email avec validation du format et de la présence
    email = StringField('Nouvelle adresse email', validators=[DataRequired(), Email()])
    submit = SubmitField('Mettre à jour l\'email')  # Button to submit the email change
    # Bouton pour soumettre le changement d'email

    # Custom validator to check if the email already exists in the database
    # Validateur personnalisé pour vérifier si l'email existe déjà dans la base de données
    def validate_email(self, email):
        if User.query.filter_by(email=email.data).first():
            raise ValidationError('Cet email est déjà utilisé.')

# Form class for changing the user's password
# Classe de formulaire pour changer le mot de passe de l'utilisateur
class ChangePasswordForm(FlaskForm):
    current_password = PasswordField('Mot de passe actuel', validators=[DataRequired()])  # Field for current password
    # Champ pour le mot de passe actuel
    new_password = PasswordField('Nouveau mot de passe', validators=[DataRequired()])  # Field for new password
    # Champ pour le nouveau mot de passe
    confirm_new_password = PasswordField('Confirmez le nouveau mot de passe', validators=[DataRequired(), EqualTo('new_password')])
    # Champ pour confirmer le nouveau mot de passe, doit correspondre au champ du nouveau mot de passe
    submit = SubmitField('Mettre à jour le mot de passe')  # Button to submit the password change
    # Bouton pour soumettre le changement de mot de passe

# Form class for deleting the user's account with confirmation
# Classe de formulaire pour supprimer le compte de l'utilisateur avec confirmation
class DeleteAccountForm(FlaskForm):
    confirm = BooleanField('Je confirme vouloir supprimer mon compte', validators=[DataRequired()])  # Confirmation checkbox
    # Case à cocher pour confirmer la suppression du compte
    submit = SubmitField('Supprimer mon compte')  # Button to submit the account deletion
    # Bouton pour soumettre la suppression du compte

# Form class for editing the user's profile with various optional and required fields
# Classe de formulaire pour modifier le profil de l'utilisateur avec divers champs optionnels et requis
class EditProfileForm(FlaskForm):
    username = StringField('Nom d\'utilisateur', validators=[DataRequired()])  # Field for username, required
    # Champ pour le nom d'utilisateur, requis
    email = StringField('Email', validators=[DataRequired(), Email()])  # Field for email, required and validated
    # Champ pour l'email, requis et validé
    first_name = StringField('Prénom')  # Field for first name
    # Champ pour le prénom
    last_name = StringField('Nom de famille')  # Field for last name
    # Champ pour le nom de famille
    country = StringField('Pays')  # Field for country
    # Champ pour le pays
    city = StringField('Ville')  # Field for city
    # Champ pour la ville
    address = StringField('Adresse')  # Field for address
    # Champ pour l'adresse
    postal_code = StringField('Code Postal')  # Field for postal code
    # Champ pour le code postal
    sex = SelectField(
        'Sexe',
        choices=[('', 'Sélectionnez'), ('Male', 'Homme'), ('Female', 'Femme'), ('Other', 'Autre')],
        validators=[Optional()]  # Optional field for selecting sex
        # Champ optionnel pour sélectionner le sexe
    )
    birth_date = DateField('Date de Naissance', format='%Y-%m-%d', validators=[Optional()])  # Optional field for birth date
    # Champ optionnel pour la date de naissance
    phone = TelField('Numéro de Téléphone')  # Field for phone number
    # Champ pour le numéro de téléphone
    display_phone = BooleanField('Afficher le numéro de téléphone')  # Checkbox for displaying phone number
    # Case à cocher pour afficher le numéro de téléphone
    display_email = BooleanField('Afficher l\'email')  # Checkbox for displaying email
    # Case à cocher pour afficher l'email
    profile_image = FileField('Photo de Profil', validators=[FileAllowed(['jpg', 'jpeg', 'png', 'gif'], 'Images uniquement!')])
    # Champ de téléchargement pour l'image de profil, limité aux formats d'image spécifiés
    cover_image = FileField('Image de Couverture', validators=[FileAllowed(['jpg', 'jpeg', 'png', 'gif'], 'Images uniquement!')])
    # Champ de téléchargement pour l'image de couverture, limité aux formats d'image spécifiés
    latitude = FloatField('Latitude')  # Field for latitude
    # Champ pour la latitude
    longitude = FloatField('Longitude')  # Field for longitude
    # Champ pour la longitude
    submit = SubmitField('Mettre à Jour')  # Button to submit the profile changes
    # Bouton pour soumettre les modifications du profil

# Form class for changing the cover photo
# Classe de formulaire pour changer la photo de couverture
class ChangeCoverPhotoForm(FlaskForm):
    cover_image = FileField('Nouvelle photo de couverture', validators=[DataRequired(), FileAllowed(['jpg', 'jpeg', 'png', 'gif'], 'Images uniquement!')])
    # Champ de téléchargement pour la nouvelle photo de couverture, requis et limité aux formats d'image spécifiés
    submit = SubmitField('Mettre à jour')  # Button to submit the cover photo change
    # Bouton pour soumettre le changement de photo de couverture

# Form class for changing the profile photo
# Classe de formulaire pour changer la photo de profil
class ChangeProfilePhotoForm(FlaskForm):
    profile_image = FileField('Nouvelle photo de profil', validators=[DataRequired(), FileAllowed(['jpg', 'jpeg', 'png', 'gif'], 'Images uniquement!')])
    # Champ de téléchargement pour la nouvelle photo de profil, requis et limité aux formats d'image spécifiés
    submit = SubmitField('Mettre à jour')  # Button to submit the profile photo change
    # Bouton pour soumettre le changement de photo de profil

# Form class for completing the user's profile with required fields
# Classe de formulaire pour compléter le profil de l'utilisateur avec des champs requis
class CompleteProfileForm(FlaskForm):
    birth_date = DateField('Date de naissance', format='%Y-%m-%d', validators=[DataRequired()])  # Required field for birth date
    # Champ requis pour la date de naissance
    sex = SelectField('Sexe', choices=[('male', 'Homme'), ('female', 'Femme'), ('other', 'Autre')], validators=[DataRequired()])
    # Champ requis pour sélectionner le sexe
    profile_image = FileField('Photo de profil', validators=[FileAllowed(['jpg', 'png', 'jpeg'], 'Images seulement!')])
    # Champ de téléchargement pour la photo de profil, limité aux formats spécifiés
    cover_image = FileField('Photo de couverture', validators=[FileAllowed(['jpg', 'png', 'jpeg'], 'Images seulement!')])
    # Champ de téléchargement pour la photo de couverture, limité aux formats spécifiés
    sports = SelectMultipleField('Sports pratiqués', choices=[], validators=[DataRequired()])  # Required multiple selection field for practiced sports
    # Champ de sélection multiple requis pour les sports pratiqués
    levels = SelectMultipleField('Niveaux', choices=[(str(i), f'{i} étoiles') for i in range(1, 6)], validators=[DataRequired()])
    # Champ de sélection multiple requis pour les niveaux (étoiles)
    submit = SubmitField('Enregistrer')  # Button to submit the completed profile
    # Bouton pour soumettre le profil complété

# Custom field for rendering multiple checkboxes in forms
# Champ personnalisé pour afficher plusieurs cases à cocher dans les formulaires
class MultiCheckboxField(QuerySelectMultipleField):
    widget = ListWidget(prefix_label=False)  # Widget for displaying a list of checkboxes
    # Widget pour afficher une liste de cases à cocher
    option_widget = CheckboxInput()  # Widget for each checkbox input
    # Widget pour chaque entrée de case à cocher
