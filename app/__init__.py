from flask import Flask
from flask_dance.contrib.facebook import make_facebook_blueprint
from flask_dance.contrib.strava import make_strava_blueprint
from app.extensions import db, migrate, bcrypt, jwt, mail, login_manager

def create_app():
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object('config.Config')

    # Initialiser les extensions
    db.init_app(app)
    migrate.init_app(app, db)
    bcrypt.init_app(app)
    jwt.init_app(app)
    mail.init_app(app)
    login_manager.init_app(app)

    # Configurer le login manager
    login_manager.login_view = 'main.login'
    login_manager.login_message_category = 'info'

    # Importer et enregistrer les blueprints
    from .routes import bp as main_bp
    from .messages import bp as messages_bp
    app.register_blueprint(main_bp)
    app.register_blueprint(messages_bp, url_prefix='/messages')

    # Création du blueprint pour Facebook OAuth
    facebook_bp = make_facebook_blueprint(
        client_id=app.config['FACEBOOK_OAUTH_CLIENT_ID'],
        client_secret=app.config['FACEBOOK_OAUTH_CLIENT_SECRET'],
        redirect_to='main.profile'
    )
    app.register_blueprint(facebook_bp, url_prefix="/facebook_login")

    # Création du blueprint pour Strava OAuth
    strava_bp = make_strava_blueprint(
        client_id=app.config['STRAVA_OAUTH_CLIENT_ID'],
        client_secret=app.config['STRAVA_OAUTH_CLIENT_SECRET'],
        redirect_to='main.profile'
    )
    app.register_blueprint(strava_bp, url_prefix="/strava_login")

    with app.app_context():
        from .models import User, Post, Sport, Rating

        @login_manager.user_loader
        def load_user(user_id):
            return User.query.get(int(user_id))

    return app
