from app.models import User
from app.extensions import db, mail
from flask_mail import Message
from flask import url_for, current_app
from itsdangerous import URLSafeTimedSerializer

def send_password_reset_email(user):
    token = generate_reset_token(user.email)
    msg = Message('Réinitialisation du mot de passe', recipients=[user.email])
    reset_url = url_for('auth.reset_password', token=token, _external=True)
    msg.body = f'Pour réinitialiser votre mot de passe, cliquez sur le lien suivant : {reset_url}'
    mail.send(msg)

def generate_reset_token(email):
    serializer = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
    return serializer.dumps(email, salt='password-reset-salt')

def register_user_if_new(provider, provider_id, email=None, username=None):
    """Vérifie si un utilisateur existe pour l'ID du fournisseur donné et le crée sinon."""
    user = User.query.filter_by(provider=provider, provider_id=provider_id).first()

    if not user:
        user = User(
            provider=provider,
            provider_id=provider_id,
            email=email,
            username=username or f"{provider}_{provider_id}"
        )
        db.session.add(user)
        db.session.commit()

    return user
