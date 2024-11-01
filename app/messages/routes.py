from flask import Blueprint

bp = Blueprint('messages', __name__)

# Ajoutez ici vos routes pour le module messages
@bp.route('/')
def index():
    return "Messages Module"
