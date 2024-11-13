import logging
from logging.config import fileConfig

from flask import current_app
from alembic import context

# Alembic configuration object to access the .ini file values.
# Objet de configuration Alembic pour accéder aux valeurs du fichier .ini.
config = context.config

# Setup logging from the config file.
# Configure les logs à partir du fichier de configuration.
fileConfig(config.config_file_name)
logger = logging.getLogger('alembic.env')

# Function to get the engine used by Flask-Migrate
# Fonction pour obtenir l'engine utilisé par Flask-Migrate
def get_engine():
    try:
        # Works for Flask-SQLAlchemy versions < 3
        # Fonctionne pour Flask-SQLAlchemy versions < 3
        return current_app.extensions['migrate'].db.get_engine()
    except (TypeError, AttributeError):
        # Works for Flask-SQLAlchemy versions >= 3
        # Fonctionne pour Flask-SQLAlchemy versions >= 3
        return current_app.extensions['migrate'].db.engine

# Function to get the URL of the engine
# Fonction pour obtenir l'URL de l'engine
def get_engine_url():
    try:
        # Returns the URL, hiding the password.
        # Retourne l'URL, masquant le mot de passe.
        return get_engine().url.render_as_string(hide_password=False).replace('%', '%%')
    except AttributeError:
        # Fallback to string conversion.
        # Conversion en chaîne de caractères par défaut.
        return str(get_engine().url).replace('%', '%%')

# Setting the main option for the SQLAlchemy URL in Alembic.
# Configuration de l'option principale pour l'URL SQLAlchemy dans Alembic.
config.set_main_option('sqlalchemy.url', get_engine_url())
target_db = current_app.extensions['migrate'].db

# Function to get the metadata of the target database
# Fonction pour obtenir les métadonnées de la base de données cible
def get_metadata():
    if hasattr(target_db, 'metadatas'):
        return target_db.metadatas[None]
    return target_db.metadata

# Function to run migrations in offline mode
# Fonction pour exécuter les migrations en mode hors ligne
def run_migrations_offline():
    """Run migrations in 'offline' mode.

    Configures the context with a URL without creating an Engine.
    Useful when DBAPI is not required.
    Configures the context and runs migrations in script output.
    """
    # Configuration du contexte avec l'URL sans créer un Engine.
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url, target_metadata=get_metadata(), literal_binds=True
    )

    with context.begin_transaction():
        context.run_migrations()

# Function to run migrations in online mode
# Fonction pour exécuter les migrations en mode en ligne
def run_migrations_online():
    """Run migrations in 'online' mode.

    Creates an Engine and associates a connection with the context.
    """
    # Callback to prevent auto-migration generation if no schema changes.
    # Callback pour empêcher la génération de migrations automatiques s'il n'y a pas de modifications.
    def process_revision_directives(context, revision, directives):
        if getattr(config.cmd_opts, 'autogenerate', False):
            script = directives[0]
            if script.upgrade_ops.is_empty():
                directives[:] = []  # Prevents migration creation
                logger.info('No changes in schema detected.')

    # Adding the callback to the configuration if not already present.
    # Ajout du callback à la configuration s'il n'est pas déjà présent.
    conf_args = current_app.extensions['migrate'].configure_args
    if conf_args.get("process_revision_directives") is None:
        conf_args["process_revision_directives"] = process_revision_directives

    connectable = get_engine()

    # Establishing a connection and running the migration.
    # Établissement d'une connexion et exécution de la migration.
    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=get_metadata(),
            **conf_args
        )

        with context.begin_transaction():
            context.run_migrations()

# Determine the mode (offline/online) and run the appropriate function.
# Détermine le mode (hors ligne/en ligne) et exécute la fonction appropriée.
if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
