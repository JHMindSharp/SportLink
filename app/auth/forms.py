"""
app/auth/forms.py

This module defines the forms used for user authentication and registration functionalities in the application.
It uses Flask-WTF for form handling and WTForms for form validation.

Components:
- `RegistrationForm`: Form for user registration with fields for personal details and validation.
- `LoginForm`: Form for user login with email and password.
- `ResetPasswordRequestForm`: Form to request a password reset by email.
- `ResetPasswordForm`: Form to reset the user's password.
"""

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, DateField, SelectField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError
from app.models import User

# Form for user registration
class RegistrationForm(FlaskForm):
    """
    This form collects user details for registration, including:
    - Username
    - Email
    - First and last names
    - Birth date
    - Gender
    - Password and confirmation
    """
    username = StringField('Nom d\'utilisateur', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    first_name = StringField('Prénom', validators=[DataRequired()])
    last_name = StringField('Nom de famille', validators=[DataRequired()])
    birth_date = DateField('Date de naissance', format='%Y-%m-%d', validators=[DataRequired()])
    gender = SelectField('Genre', choices=[('male', 'Homme'), ('female', 'Femme'), ('other', 'Autre')], validators=[DataRequired()])
    password = PasswordField('Mot de passe', validators=[DataRequired()])
    confirm_password = PasswordField('Confirmez le mot de passe', validators=[DataRequired(), EqualTo('password')])
    accept_terms = BooleanField(
        'J\'accepte les <a href="{{ url_for(\'main.privacy_policy\') }}">conditions d\'utilisation</a>', 
        validators=[DataRequired()]
    )
    submit = SubmitField('Inscription')

    # Custom validation to ensure email is unique
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Cet email est déjà utilisé.')

    # Custom validation to ensure username is unique
    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Ce nom d\'utilisateur est déjà utilisé.')

# Form for user login
class LoginForm(FlaskForm):
    """
    This form collects the user's email and password for login.
    """
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Mot de passe', validators=[DataRequired()])
    submit = SubmitField('Connexion')

# Form for requesting a password reset
class ResetPasswordRequestForm(FlaskForm):
    """
    This form collects the user's email to send a password reset link.
    """
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Réinitialiser le mot de passe')

# Form for resetting the user's password
class ResetPasswordForm(FlaskForm):
    """
    This form collects the new password and confirmation for resetting the user's password.
    """
    password = PasswordField('Nouveau mot de passe', validators=[DataRequired()])
    confirm_password = PasswordField('Confirmez le mot de passe', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Réinitialiser le mot de passe')
