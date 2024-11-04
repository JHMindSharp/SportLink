from app.models import User
from app.extensions import db

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