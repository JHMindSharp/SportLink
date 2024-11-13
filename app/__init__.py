# Importing the Flask class to create the Flask application instance
# Importation de la classe Flask pour créer l'instance de l'application Flask
from flask import Flask
# Importing Flask-Dance blueprints for Facebook OAuth integration
# Importation des blueprints Flask-Dance pour l'intégration OAuth de Facebook
from flask_dance.contrib.facebook import make_facebook_blueprint
# Importing Flask-Dance blueprint for Strava OAuth integration
# Importation du blueprint Flask-Dance pour l'intégration OAuth de Strava
from flask_dance.contrib.strava import make_strava_blueprint
# Importing initialized extensions (database, migration, bcrypt, JWT, mail, login manager)
# Importation des extensions initialisées (base de données, migration, bcrypt, JWT, mail, gestionnaire de connexion)
from app.extensions import db, migrate, bcrypt, jwt, mail, login_manager
from flask_wtf.csrf import CSRFProtect, generate_csrf
# Importing load_dotenv to load environment variables from a .env file
# Importation de load_dotenv pour charger les variables d'environnement depuis un fichier .env
from dotenv import load_dotenv


# Loading environment variables from the .env file to the environment
# Chargement des variables d'environnement depuis le fichier .env vers l'environnement
load_dotenv()


# Initializing CSRF protection for securing the app against cross-site request forgery
# Initialisation de la protection CSRF pour sécuriser l'application contre les attaques de type cross-site request forgery
csrf = CSRFProtect()

# Defining the factory function to create and configure the Flask application instance
# Définition de la fonction usine pour créer et configurer l'instance de l'application Flask
def create_app():
# Creating the Flask application instance with relative config to instance folder
# Création de l'instance de l'application Flask avec une configuration relative au dossier d'instance
    app = Flask(__name__, instance_relative_config=True)
# Loading configuration settings from a Python configuration file
# Chargement des paramètres de configuration depuis un fichier de configuration Python
    app.config.from_pyfile('config.py')


# Initializing the database extension with the Flask app
# Initialisation de l'extension de base de données avec l'application Flask
    db.init_app(app)
# Setting up the migration tool for handling database schema changes
# Configuration de l'outil de migration pour gérer les changements de schéma de base de données
    migrate.init_app(app, db)
    bcrypt.init_app(app)
    jwt.init_app(app)
    mail.init_app(app)
# Integrating the login manager for user session management
# Intégration du gestionnaire de connexion pour la gestion des sessions utilisateur
    login_manager.init_app(app)


# Enabling CSRF protection on the app
# Activation de la protection CSRF sur l'application
    csrf.init_app(app)


# Setting the default login view route for unauthorized users
# Définition de la route par défaut de la vue de connexion pour les utilisateurs non autorisés
    login_manager.login_view = 'auth.login'
# Setting the category for flashed login messages
# Définition de la catégorie des messages flash de connexion
    login_manager.login_message_category = 'info'


# Importing the authentication blueprint for registering routes
# Importation du blueprint d'authentification pour l'enregistrement des routes
    from app.auth.routes import auth_bp
    from app.profile.routes import profile_bp
    from app.posts.routes import posts_bp
    from app.messages.routes import messages_bp
    from app.news_feed.routes import news_feed_bp
    from app.main.routes import main_bp
    from app.notifications.routes import notifications_bp
    from app.events.routes import events_bp

# Registering a blueprint to include its routes in the app
# Enregistrement d'un blueprint pour inclure ses routes dans l'application
    app.register_blueprint(auth_bp, url_prefix='/auth')
# Registering a blueprint to include its routes in the app
# Enregistrement d'un blueprint pour inclure ses routes dans l'application
    app.register_blueprint(profile_bp, url_prefix='/profile')
# Registering a blueprint to include its routes in the app
# Enregistrement d'un blueprint pour inclure ses routes dans l'application
    app.register_blueprint(posts_bp, url_prefix='/posts')
# Registering a blueprint to include its routes in the app
# Enregistrement d'un blueprint pour inclure ses routes dans l'application
    app.register_blueprint(messages_bp, url_prefix='/messages')
# Registering a blueprint to include its routes in the app
# Enregistrement d'un blueprint pour inclure ses routes dans l'application
    app.register_blueprint(news_feed_bp, url_prefix='/news_feed')
# Registering a blueprint to include its routes in the app
# Enregistrement d'un blueprint pour inclure ses routes dans l'application
    app.register_blueprint(main_bp)
# Registering a blueprint to include its routes in the app
# Enregistrement d'un blueprint pour inclure ses routes dans l'application
    app.register_blueprint(notifications_bp, url_prefix='/notifications')
# Registering a blueprint to include its routes in the app
# Enregistrement d'un blueprint pour inclure ses routes dans l'application
    app.register_blueprint(events_bp, url_prefix='/events')


    facebook_bp = make_facebook_blueprint(
        client_id=app.config['FACEBOOK_OAUTH_CLIENT_ID'],
        client_secret=app.config['FACEBOOK_OAUTH_CLIENT_SECRET'],
        redirect_to='auth.oauth_facebook'
    )
# Registering a blueprint to include its routes in the app
# Enregistrement d'un blueprint pour inclure ses routes dans l'application
    app.register_blueprint(facebook_bp, url_prefix='/facebook_login')


    strava_bp = make_strava_blueprint(
        client_id=app.config['STRAVA_OAUTH_CLIENT_ID'],
        client_secret=app.config['STRAVA_OAUTH_CLIENT_SECRET'],
        scope='read,profile:read_all',
        redirect_to='auth.oauth_strava'
    )
# Registering a blueprint to include its routes in the app
# Enregistrement d'un blueprint pour inclure ses routes dans l'application
    app.register_blueprint(strava_bp, url_prefix='/strava_login')


    with app.app_context():
        from app.models import User

        @login_manager.user_loader
        def load_user(user_id):
            return User.query.get(int(user_id))


    from app.auth.forms import LoginForm, RegistrationForm

    @app.context_processor
    def inject_globals():
        return dict(
            login_form=LoginForm(),
            register_form=RegistrationForm(),
            csrf_token=generate_csrf
        )

    return app
