from datetime import datetime
from flask_login import UserMixin
from app import db, bcrypt

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<Post {self.id} - User {self.user_id}>'

class User(db.Model, UserMixin):
    """User model for storing user information."""
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(
        db.String(64),
        index=True,
        unique=True,
        nullable=False)
    email = db.Column(db.String(120), index=True, unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    profile_image = db.Column(db.String(128), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    profile_completed = db.Column(db.Boolean, default=False)  # Champ ajouté pour vérifier si le profil est complété
    email_confirmed = db.Column(db.Boolean, default=False)  # Champ ajouté pour la confirmation d'email

    def set_password(self, password):
        """Generate a password hash using bcrypt."""
        self.password_hash = bcrypt.generate_password_hash(
            password).decode('utf-8')

    def check_password(self, password):
        """Check the password hash against the provided password."""
        return bcrypt.check_password_hash(self.password_hash, password)
