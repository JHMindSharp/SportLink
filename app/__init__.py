from flask import Flask
from flask_dance.contrib.facebook import make_facebook_blueprint
from flask_dance.contrib.strava import make_strava_blueprint
from app.extensions import db, migrate, bcrypt, jwt, mail, login_manager
from app.main.routes import main_bp

def create_app():
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object('instance.config.Config')

    # Initialisation des extensions
    db.init_app(app)
    migrate.init_app(app, db)
    bcrypt.init_app(app)
    jwt.init_app(app)
    mail.init_app(app)
    login_manager.init_app(app)

    # Configurer le login manager
    login_manager.login_view = 'auth.login'
    login_manager.login_message_category = 'info'

    # Enregistrer les blueprints
    from app.auth.routes import auth_bp
    from app.profile.routes import profile_bp
    from app.posts.routes import posts_bp
    from app.messages.routes import messages_bp
    from app.news_feed.routes import news_feed_bp
    from app.main.routes import main_bp
    
    app.register_blueprint(news_feed_bp, url_prefix='/news_feed')
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(profile_bp, url_prefix='/profile')
    app.register_blueprint(posts_bp, url_prefix='/posts')
    app.register_blueprint(messages_bp, url_prefix='/messages')
    app.register_blueprint(main_bp, url_prefix='/')

    # OAuth Facebook
    facebook_bp = make_facebook_blueprint(
        client_id=app.config['FACEBOOK_OAUTH_CLIENT_ID'],
        client_secret=app.config['FACEBOOK_OAUTH_CLIENT_SECRET'],
        redirect_to='profile.edit_profile'
    )
    app.register_blueprint(facebook_bp, url_prefix='/facebook_login')

    # OAuth Strava
    strava_bp = make_strava_blueprint(
        client_id=app.config['STRAVA_OAUTH_CLIENT_ID'],
        client_secret=app.config['STRAVA_OAUTH_CLIENT_SECRET'],
        redirect_to='profile.edit_profile'
    )
    app.register_blueprint(strava_bp, url_prefix='/strava_login')

    # Charger l'utilisateur pour le login manager
    with app.app_context():
        from app.models import User

        @login_manager.user_loader
        def load_user(user_id):
            return User.query.get(int(user_id))

    return app
