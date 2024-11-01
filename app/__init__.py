from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from flask_mail import Mail
from flask_login import LoginManager

# Initialisation des extensions

db = SQLAlchemy()
migrate = Migrate()
bcrypt = Bcrypt()
jwt = JWTManager()
mail = Mail()
login_manager = LoginManager()

login_manager.login_view = 'main.login'
login_manager.login_message_category = 'info'

def create_app():
    """Create and configure the Flask application."""
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object('config.Config')
    app.config.from_pyfile('config.py', silent=True)

    # Initialiser les extensions
    db.init_app(app)
    migrate.init_app(app, db)
    bcrypt.init_app(app)
    jwt.init_app(app)
    mail.init_app(app)
    login_manager.init_app(app)

    # Importer les modèles après avoir initialisé l'application pour éviter les importations circulaires
    from .models import User

    # Définir la fonction de rappel pour charger l'utilisateur
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    with app.app_context():
        # Importer et enregistrer le blueprint
        from .routes import bp as main_bp
        app.register_blueprint(main_bp)
        db.create_all()

    return app
