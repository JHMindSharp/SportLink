from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from flask_mail import Mail
from flask_login import LoginManager

# Initialize the SQLAlchemy instance for handling database operations
# Initialise l'instance SQLAlchemy pour gérer les opérations de base de données
db = SQLAlchemy()

# Initialize the migration tool for database schema changes
# Initialise l'outil de migration pour les changements de schéma de base de données
migrate = Migrate()

# Initialize Bcrypt for password hashing and verification
# Initialise Bcrypt pour le hachage et la vérification des mots de passe
bcrypt = Bcrypt()

# Initialize the JWT Manager for managing JSON Web Tokens for secure API authentication
# Initialise le gestionnaire JWT pour gérer les JSON Web Tokens pour l'authentification sécurisée des API
jwt = JWTManager()

# Initialize the Mail extension for sending emails
# Initialise l'extension Mail pour l'envoi de courriels
mail = Mail()

# Initialize the Login Manager for handling user sessions and authentication
# Initialise le gestionnaire de connexion pour gérer les sessions utilisateurs et l'authentification
login_manager = LoginManager()
