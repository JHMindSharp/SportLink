from flask import Blueprint

posts_bp = Blueprint('posts', __name__)

from app.posts import routes
