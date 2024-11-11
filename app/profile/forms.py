from flask_wtf import FlaskForm
from wtforms import (
    StringField, PasswordField, SubmitField, BooleanField, FileField,
    SelectField, DateField, HiddenField, TelField, FloatField
)
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError, Optional
from flask_wtf.file import FileAllowed
from app.models import User

class ChangeEmailForm(FlaskForm):
    email = StringField('Nouvelle adresse email', validators=[DataRequired(), Email()])
    submit = SubmitField('Mettre à jour l\'email')

    def validate_email(self, email):
        if User.query.filter_by(email=email.data).first():
            raise ValidationError('Cet email est déjà utilisé.')

class ChangePasswordForm(FlaskForm):
    current_password = PasswordField('Mot de passe actuel', validators=[DataRequired()])
    new_password = PasswordField('Nouveau mot de passe', validators=[DataRequired()])
    confirm_new_password = PasswordField('Confirmez le nouveau mot de passe', validators=[DataRequired(), EqualTo('new_password')])
    submit = SubmitField('Mettre à jour le mot de passe')

class DeleteAccountForm(FlaskForm):
    confirm = BooleanField('Je confirme vouloir supprimer mon compte', validators=[DataRequired()])
    submit = SubmitField('Supprimer mon compte')

class EditProfileForm(FlaskForm):
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
    cover_image = FileField('Nouvelle photo de couverture', validators=[DataRequired(), FileAllowed(['jpg', 'jpeg', 'png', 'gif'], 'Images uniquement!')])
    submit = SubmitField('Mettre à jour')

class ChangeProfilePhotoForm(FlaskForm):
    profile_image = FileField('Nouvelle photo de profil', validators=[DataRequired(), FileAllowed(['jpg', 'jpeg', 'png', 'gif'], 'Images uniquement!')])
    submit = SubmitField('Mettre à jour')

class CompleteProfileForm(FlaskForm):
    birth_date = DateField('Date de naissance', validators=[DataRequired()])
    sex = SelectField(
        'Sexe',
        choices=[('male', 'Homme'), ('female', 'Femme'), ('other', 'Autre')],
        validators=[DataRequired()]
    )
    submit = SubmitField('Enregistrer')
