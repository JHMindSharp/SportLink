from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, DateField, SelectField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError
from app.models import User

# Form class for user registration with input validation
# Classe de formulaire pour l'enregistrement des utilisateurs avec validation des saisies
class RegistrationForm(FlaskForm):
    # Field for the username, required for unique identification of the user
    # Champ pour le nom d'utilisateur, requis pour l'identification unique de l'utilisateur
    username = StringField('Nom d\'utilisateur', validators=[DataRequired()])
    
    # Field for the user's email with validation to ensure it is provided and formatted correctly
    # Champ pour l'email de l'utilisateur avec validation pour garantir qu'il est fourni et correctement formaté
    email = StringField('Email', validators=[DataRequired(), Email()])
    
    # Field for the user's first name, required for user registration
    # Champ pour le prénom de l'utilisateur, requis pour l'enregistrement
    first_name = StringField('Prénom', validators=[DataRequired()])
    
    # Field for the user's last name, required for user registration
    # Champ pour le nom de famille de l'utilisateur, requis pour l'enregistrement
    last_name = StringField('Nom de famille', validators=[DataRequired()])
    
    # Field for the user's birth date, required and formatted as YYYY-MM-DD
    # Champ pour la date de naissance de l'utilisateur, requis et formaté en AAAA-MM-JJ
    birth_date = DateField('Date de naissance', format='%Y-%m-%d', validators=[DataRequired()])
    
    # Dropdown field for selecting gender with predefined choices
    # Champ déroulant pour sélectionner le genre avec des choix prédéfinis
    gender = SelectField('Genre', choices=[('male', 'Homme'), ('female', 'Femme'), ('other', 'Autre')], validators=[DataRequired()])
    
    # Field for entering the password with a requirement for validation
    # Champ pour saisir le mot de passe avec une exigence de validation
    password = PasswordField('Mot de passe', validators=[DataRequired()])
    
    # Field to confirm the password, must match the initial password field
    # Champ pour confirmer le mot de passe, doit correspondre au champ de mot de passe initial
    confirm_password = PasswordField('Confirmez le mot de passe', validators=[DataRequired(), EqualTo('password')])
    
    # Checkbox field to accept terms of service, required for registration
    # Champ de case à cocher pour accepter les conditions d'utilisation, requis pour l'enregistrement
    accept_terms = BooleanField('J\'accepte les <a href="{{ url_for(\'main.privacy_policy\') }}">conditions d\'utilisation</a>', validators=[DataRequired()])
    
    # Submit button to submit the form
    # Bouton de soumission pour envoyer le formulaire
    submit = SubmitField('Inscription')

    # Custom validator to ensure the email is unique
    # Validateur personnalisé pour garantir que l'email est unique
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Cet email est déjà utilisé.')

    # Custom validator to ensure the username is unique
    # Validateur personnalisé pour garantir que le nom d'utilisateur est unique
    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Ce nom d\'utilisateur est déjà utilisé.')

# Form class for user login with basic input fields
# Classe de formulaire pour la connexion des utilisateurs avec des champs de saisie basiques
class LoginForm(FlaskForm):
    # Field for the user's email with validation
    # Champ pour l'email de l'utilisateur avec validation
    email = StringField('Email', validators=[DataRequired(), Email()])
    
    # Field for entering the user's password
    # Champ pour saisir le mot de passe de l'utilisateur
    password = PasswordField('Mot de passe', validators=[DataRequired()])
    
    # Submit button for logging in
    # Bouton de soumission pour la connexion
    submit = SubmitField('Connexion')

# Form class for requesting password reset
# Classe de formulaire pour demander la réinitialisation du mot de passe
class ResetPasswordRequestForm(FlaskForm):
    # Field for the user's email to send the reset link
    # Champ pour l'email de l'utilisateur pour envoyer le lien de réinitialisation
    email = StringField('Email', validators=[DataRequired(), Email()])
    
    # Submit button to request password reset
    # Bouton de soumission pour demander la réinitialisation du mot de passe
    submit = SubmitField('Réinitialiser le mot de passe')

# Form class for resetting the password with validation
# Classe de formulaire pour réinitialiser le mot de passe avec validation
class ResetPasswordForm(FlaskForm):
    # Field for entering the new password
    # Champ pour saisir le nouveau mot de passe
    password = PasswordField('Nouveau mot de passe', validators=[DataRequired()])
    
    # Field to confirm the new password, must match the password field
    # Champ pour confirmer le nouveau mot de passe, doit correspondre au champ de mot de passe
    confirm_password = PasswordField('Confirmez le mot de passe', validators=[DataRequired(), EqualTo('password')])
    
    # Submit button to reset the password
    # Bouton de soumission pour réinitialiser le mot de passe
    submit = SubmitField('Réinitialiser le mot de passe')
