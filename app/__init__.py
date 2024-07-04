from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager

db = SQLAlchemy()
migrate = Migrate()
bcrypt = Bcrypt()
jwt = JWTManager()  # Initialisation de JWTManager

def create_app():
    """Create and configure the app."""
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object('config.Config')
    app.config.from_pyfile('config.py', silent=True)

    db.init_app(app)
    migrate.init_app(app, db)
    bcrypt.init_app(app)
    jwt.init_app(app)  # Ajout de l'initialisation de JWTManager

    with app.app_context():
        from . import models

        # Enregistrez le blueprint une seule fois
        from .routes import bp as main_bp
        app.register_blueprint(main_bp)
        db.create_all()

    return app
