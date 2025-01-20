"""
app/profile/forms.py

This module defines forms related to user profile management in the SportLink application.
It includes functionalities for editing profile information, changing passwords, updating profile and cover photos,
completing the profile, and deleting the account.

Components:
- `ChangeEmailForm`: Form to change the user's email.
- `ChangePasswordForm`: Form to change the user's password.
- `DeleteAccountForm`: Form to confirm account deletion.
- `EditProfileForm`: Form to edit profile details.
- `ChangeCoverPhotoForm`: Form to update the cover photo.
- `ChangeProfilePhotoForm`: Form to update the profile photo.
- `CompleteProfileForm`: Form to complete profile details.
- `MultiCheckboxField`: Custom field for multi-checkbox selection.
"""

from flask_wtf import FlaskForm
from wtforms import (
    StringField, PasswordField, SubmitField, BooleanField, FileField,
    SelectField, DateField, HiddenField, TelField, FloatField, SelectMultipleField
)
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError, Optional
from flask_wtf.file import FileAllowed
from app.models import User
from wtforms_sqlalchemy.fields import QuerySelectMultipleField
from wtforms.widgets import ListWidget, CheckboxInput

class ChangeEmailForm(FlaskForm):
    """
    Form to allow users to change their email address.

    Fields:
    - `email`: Input for the new email (validated for format and uniqueness).
    - `submit`: Submit button to confirm email update.

    Methods:
    - `validate_email`: Checks if the email is already in use.
    """
    email = StringField('Nouvelle adresse email', validators=[DataRequired(), Email()])
    submit = SubmitField('Mettre à jour l\'email')

    def validate_email(self, email):
        if User.query.filter_by(email=email.data).first():
            raise ValidationError('Cet email est déjà utilisé.')

class ChangePasswordForm(FlaskForm):
    """
    Form to allow users to change their password.

    Fields:
    - `current_password`: Input for the current password (required).
    - `new_password`: Input for the new password (required).
    - `confirm_new_password`: Confirmation for the new password (must match).
    - `submit`: Submit button to confirm password update.
    """
    current_password = PasswordField('Mot de passe actuel', validators=[DataRequired()])
    new_password = PasswordField('Nouveau mot de passe', validators=[DataRequired()])
    confirm_new_password = PasswordField('Confirmez le nouveau mot de passe', validators=[DataRequired(), EqualTo('new_password')])
    submit = SubmitField('Mettre à jour le mot de passe')

class DeleteAccountForm(FlaskForm):
    """
    Form to confirm account deletion.

    Fields:
    - `confirm`: Checkbox to confirm the action (required).
    - `submit`: Submit button to delete the account.
    """
    confirm = BooleanField('Je confirme vouloir supprimer mon compte', validators=[DataRequired()])
    submit = SubmitField('Supprimer mon compte')

class EditProfileForm(FlaskForm):
    """
    Form to edit user profile details.

    Fields include:
    - Basic information (username, email, first/last name, address, phone, etc.).
    - Profile and cover images (optional, restricted to image formats).
    - Location data (latitude, longitude).
    - Boolean fields for displaying phone and email publicly.
    - `submit`: Submit button to update the profile.
    """
    username = StringField('Nom d\'utilisateur', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    first_name = StringField('Prénom')
    last_name = StringField('Nom de famille')
    country = StringField('Pays')
    city = StringField('Ville')
    address = StringField('Adresse')
    postal_code = StringField('Code Postal')
    sex = SelectField(
        'Sexe',
        choices=[
            ('', 'Sélectionnez'),
            ('Male', 'Homme'),
            ('Female', 'Femme'),
            ('Other', 'Autre')
        ],
        validators=[Optional()]
    )
    birth_date = DateField('Date de Naissance', format='%Y-%m-%d', validators=[Optional()])
    phone = TelField('Numéro de Téléphone')
    display_phone = BooleanField('Afficher le numéro de téléphone')
    display_email = BooleanField('Afficher l\'email')
    profile_image = FileField('Photo de Profil', validators=[FileAllowed(['jpg', 'jpeg', 'png', 'gif'], 'Images uniquement!')])
    cover_image = FileField('Image de Couverture', validators=[FileAllowed(['jpg', 'jpeg', 'png', 'gif'], 'Images uniquement!')])
    latitude = FloatField('Latitude')
    longitude = FloatField('Longitude')
    submit = SubmitField('Mettre à Jour')

class ChangeCoverPhotoForm(FlaskForm):
    """
    Form to update the user's cover photo.

    Fields:
    - `cover_image`: File upload field for the new cover photo (required, image formats only).
    - `submit`: Submit button to update the cover photo.
    """
    cover_image = FileField('Nouvelle photo de couverture', validators=[DataRequired(), FileAllowed(['jpg', 'jpeg', 'png', 'gif'], 'Images uniquement!')])
    submit = SubmitField('Mettre à jour')

class ChangeProfilePhotoForm(FlaskForm):
    """
    Form to update the user's profile photo.

    Fields:
    - `profile_image`: File upload field for the new profile photo (required, image formats only).
    - `submit`: Submit button to update the profile photo.
    """
    profile_image = FileField('Nouvelle photo de profil', validators=[DataRequired(), FileAllowed(['jpg', 'jpeg', 'png', 'gif'], 'Images uniquement!')])
    submit = SubmitField('Mettre à jour')

class CompleteProfileForm(FlaskForm):
    """
    Form to complete the user's profile.

    Fields:
    - `birth_date`: Date field for the user's birth date (required).
    - `sex`: Dropdown to select gender (required).
    - `profile_image`: File upload for profile photo (optional, image formats only).
    - `cover_image`: File upload for cover photo (optional, image formats only).
    - `sports`: Multi-select field for sports practiced (required).
    - `levels`: Multi-select field for experience levels (1 to 5 stars, required).
    - `submit`: Submit button to save profile details.
    """
    birth_date = DateField('Date de naissance', format='%Y-%m-%d', validators=[DataRequired()])
    sex = SelectField('Sexe', choices=[('male', 'Homme'), ('female', 'Femme'), ('other', 'Autre')], validators=[DataRequired()])
    profile_image = FileField('Photo de profil', validators=[FileAllowed(['jpg', 'png', 'jpeg'], 'Images seulement!')])
    cover_image = FileField('Photo de couverture', validators=[FileAllowed(['jpg', 'png', 'jpeg'], 'Images seulement!')])
    sports = SelectMultipleField('Sports pratiqués', choices=[], validators=[DataRequired()])
    levels = SelectMultipleField('Niveaux', choices=[(str(i), f'{i} étoiles') for i in range(1, 6)], validators=[DataRequired()])
    submit = SubmitField('Enregistrer')

class MultiCheckboxField(QuerySelectMultipleField):
    """
    Custom field for rendering multiple checkboxes in a form.

    - Inherits from `QuerySelectMultipleField`.
    - Uses `ListWidget` and `CheckboxInput` for rendering.
    """
    widget = ListWidget(prefix_label=False)
    option_widget = CheckboxInput()

class ChangePhotoForm(FlaskForm):
    file = FileField('Sélectionnez une photo', validators=[DataRequired()])
    submit = SubmitField('Changer la photo')
    