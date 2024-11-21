"""
app/__init__.py

This module initializes the Flask application and configures its extensions, blueprints, and other components.
"""

from flask import Flask
from flask_dance.contrib.facebook import make_facebook_blueprint
from flask_dance.contrib.strava import make_strava_blueprint
from app.extensions import db, migrate, bcrypt, jwt, mail, login_manager
from flask_wtf.csrf import CSRFProtect, generate_csrf
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Initialize CSRF protection
csrf = CSRFProtect()

def create_app():
    """
    Create and configure the Flask application.
    Returns:
        app (Flask): The configured Flask app.
    """
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_pyfile('config.py')
    
    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    bcrypt.init_app(app)
    jwt.init_app(app)
    mail.init_app(app)
    login_manager.init_app(app)
    
    # Enable CSRF protection for the app
    csrf.init_app(app)

    # Configure Flask-Login
    login_manager.login_view = 'auth.login'
    login_manager.login_message_category = 'info'
    
    # Register blueprints for modular routing
    from app.auth.routes import auth_bp
    from app.profile.routes import profile_bp
    from app.posts.routes import posts_bp
    from app.messages.routes import messages_bp
    from app.news_feed.routes import news_feed_bp
    from app.main.routes import main_bp
    from app.notifications.routes import notifications_bp
    from app.events.routes import events_bp
    
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(profile_bp, url_prefix='/profile')
    app.register_blueprint(posts_bp, url_prefix='/posts')
    app.register_blueprint(messages_bp, url_prefix='/messages')
    app.register_blueprint(news_feed_bp, url_prefix='/news_feed')
    app.register_blueprint(main_bp)
    app.register_blueprint(notifications_bp, url_prefix='/notifications')
    app.register_blueprint(events_bp, url_prefix='/events')
    
    # Configure OAuth for Facebook
    facebook_bp = make_facebook_blueprint(
        client_id=app.config['FACEBOOK_OAUTH_CLIENT_ID'],
        client_secret=app.config['FACEBOOK_OAUTH_CLIENT_SECRET'],
        redirect_to='auth.oauth_facebook'
    )
    app.register_blueprint(facebook_bp, url_prefix='/facebook_login')
    
    # Configure OAuth for Strava
    strava_bp = make_strava_blueprint(
        client_id=app.config['STRAVA_OAUTH_CLIENT_ID'],
        client_secret=app.config['STRAVA_OAUTH_CLIENT_SECRET'],
        scope='read,profile:read_all',
        redirect_to='auth.oauth_strava'
    )
    app.register_blueprint(strava_bp, url_prefix='/strava_login')
    
    # Configure user loader for Flask-Login
    with app.app_context():
        from app.models import User
        
        @login_manager.user_loader
        def load_user(user_id):
            """
            Load a user by ID for Flask-Login.
            Args:
                user_id (int): The ID of the user.
            Returns:
                User: The user instance.
            """
            return User.query.get(int(user_id))

    # Inject global variables such as forms and CSRF tokens into templates
    from app.auth.forms import LoginForm, RegistrationForm
    
    @app.context_processor
    def inject_globals():
        """
        Inject global variables into templates.
        Returns:
            dict: A dictionary of global variables.
        """
        return dict(
            login_form=LoginForm(),
            register_form=RegistrationForm(),
            csrf_token=generate_csrf
        )
    
    return app
