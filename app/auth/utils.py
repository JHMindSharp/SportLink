from app.models import User
from app.extensions import db, mail
from flask_mail import Message
from flask import url_for, current_app
from itsdangerous import URLSafeTimedSerializer

# Sends a password reset email to the specified user
# Envoie un courriel de réinitialisation de mot de passe à l'utilisateur spécifié
def send_password_reset_email(user):
    # Generates a secure token for password reset using the user's email
    # Génère un jeton sécurisé pour la réinitialisation du mot de passe en utilisant l'email de l'utilisateur
    token = generate_reset_token(user.email)
    
    # Creates a message with the reset URL to be sent via email
    # Crée un message contenant l'URL de réinitialisation à envoyer par courriel
    msg = Message('Réinitialisation du mot de passe', recipients=[user.email])
    reset_url = url_for('auth.reset_password', token=token, _external=True)
    msg.body = f'Pour réinitialiser votre mot de passe, cliquez sur le lien suivant : {reset_url}'
    
    # Sends the email with the reset URL to the user
    # Envoie le courriel contenant l'URL de réinitialisation à l'utilisateur
    mail.send(msg)

# Generates a token for secure actions such as password resets
# Génère un jeton pour des actions sécurisées telles que la réinitialisation de mot de passe
def generate_reset_token(email):
    # Initializes a serializer with the app's secret key to create secure tokens
    # Initialise un sérialiseur avec la clé secrète de l'application pour créer des jetons sécurisés
    serializer = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
    return serializer.dumps(email, salt='password-reset-salt')

# Checks if a user exists for a given provider ID; creates one if not
# Vérifie si un utilisateur existe pour un ID de fournisseur donné ; le crée sinon
def register_user_if_new(provider, provider_id, email=None, username=None):
    # Queries the database for an existing user with the specified provider and ID
    # Interroge la base de données pour un utilisateur existant avec le fournisseur et l'ID spécifiés
    user = User.query.filter_by(provider=provider, provider_id=provider_id).first()

    # If no user is found, creates a new user with the provided details
    # Si aucun utilisateur n'est trouvé, crée un nouvel utilisateur avec les détails fournis
    if not user:
        user = User(
            provider=provider,
            provider_id=provider_id,
            email=email,
            username=username or f"{provider}_{provider_id}"  # Sets a default username if none is provided
            # Définit un nom d'utilisateur par défaut si aucun n'est fourni
        )
        # Adds the new user to the session and commits the transaction to the database
        # Ajoute le nouvel utilisateur à la session et confirme la transaction dans la base de données
        db.session.add(user)
        db.session.commit()

    # Returns the user, either existing or newly created
    # Retourne l'utilisateur, existant ou nouvellement créé
    return user
