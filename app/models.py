from datetime import datetime, date
from flask_login import UserMixin
from app.extensions import db, bcrypt
from sqlalchemy import UniqueConstraint

# Association table for user sports (many-to-many relationship) with level
class UserSport(db.Model):
    __tablename__ = 'user_sport'
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    sport_id = db.Column(db.Integer, db.ForeignKey('sport.id'), primary_key=True)
    level = db.Column(db.Integer, nullable=False)  # Level from 1 to 5

class Sport(db.Model):
    """Model representing a sport."""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False, unique=True)

    def __repr__(self):
        return f'<Sport {self.name}>'

# Table d'association pour les amis
friends = db.Table('friends',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('friend_id', db.Integer, db.ForeignKey('user.id'))
)

class Rating(db.Model):
    """Model representing a rating between users."""
    id = db.Column(db.Integer, primary_key=True)
    rater_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    rated_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<Rating {self.rating} from User {self.rater_id} to User {self.rated_id}>'

class Post(db.Model):
    """Model representing a post."""
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    content_type = db.Column(db.String(20), nullable=False, default='free')
    title = db.Column(db.String(255), nullable=True)
    subtitle = db.Column(db.String(255), nullable=True)
    content = db.Column(db.Text, nullable=False)
    image = db.Column(db.String(255), nullable=True)
    video = db.Column(db.String(255), nullable=True)
    music = db.Column(db.String(255), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    visibility = db.Column(db.String(10), nullable=False, default='public')

    author = db.relationship('User', back_populates='posts')

    def __repr__(self):
        return f'<Post {self.id} - User {self.user_id}>'

class Notification(db.Model):
    """Model representing a notification."""
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    message = db.Column(db.String(255), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    is_read = db.Column(db.Boolean, default=False)

    user = db.relationship('User', back_populates='notifications')

    def __repr__(self):
        return f'<Notification {self.id} for User {self.user_id}>'

class Message(db.Model):
    """Model representing a message between users."""
    id = db.Column(db.Integer, primary_key=True)
    sender_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    recipient_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    body = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    sender = db.relationship('User', foreign_keys=[sender_id], backref='sent_messages')
    recipient = db.relationship('User', foreign_keys=[recipient_id], backref='received_messages')

    def __repr__(self):
        return f'<Message {self.id}>'

class User(db.Model, UserMixin):
    """Model representing a user."""
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True, nullable=False)
    email = db.Column(db.String(120), index=True, unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    profile_image = db.Column(db.String(255), nullable=True)
    cover_image = db.Column(db.String(255), nullable=True)
    country = db.Column(db.String(100), nullable=True)
    city = db.Column(db.String(100), nullable=True)
    address = db.Column(db.String(200), nullable=True)
    postal_code = db.Column(db.String(20), nullable=True)
    sex = db.Column(db.String(10), nullable=True)
    birth_date = db.Column(db.Date, nullable=True)
    phone = db.Column(db.String(20), nullable=True)
    display_phone = db.Column(db.Boolean, default=False)
    display_email = db.Column(db.Boolean, default=False)
    pending_email = db.Column(db.String(120), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    profile_completed = db.Column(db.Boolean, default=False)
    email_confirmed = db.Column(db.Boolean, default=False)
    provider = db.Column(db.String(50), nullable=True)
    provider_id = db.Column(db.String(100), nullable=True, unique=True)
    latitude = db.Column(db.Float, nullable=True)
    longitude = db.Column(db.Float, nullable=True)
    strava_id = db.Column(db.String(64), nullable=True)
    facebook_id = db.Column(db.String(64), nullable=True)
    __table_args__ = (
        db.UniqueConstraint('strava_id', name='uq_user_strava_id'),
        db.UniqueConstraint('facebook_id', name='uq_user_facebook_id'),
    )
    # Relationships
    notifications = db.relationship('Notification', back_populates='user', lazy='dynamic')
    sports = db.relationship('UserSport', backref='user', lazy='dynamic')
    posts = db.relationship('Post', back_populates='author', lazy='dynamic')
    ratings_received = db.relationship('Rating', foreign_keys='Rating.rated_id', backref='rated_user', lazy='dynamic')
    ratings_given = db.relationship('Rating', foreign_keys='Rating.rater_id', backref='rater_user', lazy='dynamic')
    friends = db.relationship(
        'User', secondary=friends,
        primaryjoin=(friends.c.user_id == id),
        secondaryjoin=(friends.c.friend_id == id),
        backref=db.backref('friend_of', lazy='dynamic'),
        lazy='dynamic'
    )

    def is_friend(self, user):
        return self.friends.filter(friends.c.friend_id == user.id).count() > 0

    def set_password(self, password):
        """Generate a password hash using bcrypt."""
        self.password_hash = bcrypt.generate_password_hash(password).decode('utf-8')

    def check_password(self, password):
        """Check the password hash against the provided password."""
        return bcrypt.check_password_hash(self.password_hash, password)

    @property
    def age(self):
        """Calculate age based on birth_date."""
        if self.birth_date:
            today = date.today()
            return today.year - self.birth_date.year - (
                (today.month, today.day) < (self.birth_date.month, self.birth_date.day)
            )
        else:
            return None

    @property
    def average_rating(self):
        """Calculate average rating."""
        total_ratings = self.ratings_received.count()
        if total_ratings > 0:
            sum_ratings = sum([rating.rating for rating in self.ratings_received])
            return round(sum_ratings / total_ratings, 1)
        else:
            return None

    def get_sport_level(self, sport_id):
        """Get the level of the user for a specific sport."""
        user_sport = self.sports.filter_by(sport_id=sport_id).first()
        if user_sport:
            return user_sport.level
        else:
            return None

    def __repr__(self):
        return f'<User {self.username}>'
