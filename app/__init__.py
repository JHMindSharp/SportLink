from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager

# Initialize the extensions
db = SQLAlchemy()
migrate = Migrate()
bcrypt = Bcrypt()
jwt = JWTManager()  # Initialize JWTManager


def create_app():
    """Create and configure the Flask application."""
    # Create the Flask application instance
    app = Flask(__name__, instance_relative_config=True)

    # Load the default configuration
    app.config.from_object('config.Config')

    # Load the instance configuration, if it exists, when not testing
    app.config.from_pyfile('config.py', silent=True)

    # Initialize the extensions with the app instance
    db.init_app(app)
    migrate.init_app(app, db)
    bcrypt.init_app(app)
    jwt.init_app(app)  # Initialize JWTManager with the app instance

    # Create the application context
    with app.app_context():
        # Import the models
        from . import models

        # Register the blueprint
        from .routes import bp as main_bp
        app.register_blueprint(main_bp)

        # Create all database tables
        db.create_all()

    return app
