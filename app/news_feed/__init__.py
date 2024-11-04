from flask import Blueprint

news_feed_bp = Blueprint('news_feed', __name__)

from app.news_feed import routes
