from flask import Blueprint, render_template, request
from flask_login import login_required, current_user
from app.models import Post
from app.extensions import db

news_feed_bp = Blueprint('news_feed', __name__, template_folder='templates/news_feed')

@news_feed_bp.route('/', methods=['GET'])
@login_required
def news_feed():
    # Get IDs of current user's friends
    friends_ids = [friend.id for friend in current_user.friends]
    # Include current user
    friends_ids.append(current_user.id)
    # Get posts from friends and current user, public posts, ordered by creation date
    posts = Post.query.filter(
        (Post.user_id.in_(friends_ids)) &
        ((Post.visibility == 'public') | (Post.user_id == current_user.id))
    ).order_by(Post.created_at.desc()).all()
    return render_template('news_feed/news_feed.html', posts=posts)
