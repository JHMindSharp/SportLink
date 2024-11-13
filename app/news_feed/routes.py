from flask import Blueprint, render_template, request
from flask_login import login_required, current_user
from app.models import Post
from app.extensions import db

# Define the blueprint for handling news feed routes and templates
# Définition du blueprint pour gérer les routes et modèles du fil d'actualité
news_feed_bp = Blueprint('news_feed', __name__, template_folder='templates/news_feed')

@news_feed_bp.route('/', methods=['GET'])
@login_required  # Ensures that only authenticated users can access the news feed
# S'assure que seuls les utilisateurs authentifiés peuvent accéder au fil d'actualité
def news_feed():
    # Retrieve the IDs of the current user's friends
    # Récupère les identifiants des amis de l'utilisateur actuel
    friends_ids = [friend.id for friend in current_user.friends]
    
    # Add the current user's ID to include their own posts in the feed
    # Ajoute l'identifiant de l'utilisateur actuel pour inclure ses propres publications dans le fil d'actualité
    friends_ids.append(current_user.id)
    
    # Query the database for posts made by the user and their friends, ensuring public or user-specific visibility
    # Interroge la base de données pour obtenir les publications de l'utilisateur et de ses amis, en assurant une visibilité publique ou spécifique à l'utilisateur
    posts = Post.query.filter(
        (Post.user_id.in_(friends_ids)) &  # Check if the post's user ID is in the list of friend IDs or the current user
        ((Post.visibility == 'public') | (Post.user_id == current_user.id))  # Ensure the post is public or belongs to the current user
        # Vérifie si l'ID de l'utilisateur de la publication est dans la liste des amis ou celui de l'utilisateur actuel
        # S'assure que la publication est publique ou appartient à l'utilisateur actuel
    ).order_by(Post.created_at.desc()).all()  # Order the posts by creation date, from newest to oldest
    # Trie les publications par date de création, de la plus récente à la plus ancienne

    # Render the news feed template and pass the retrieved posts for display
    # Affiche le modèle du fil d'actualité et passe les publications récupérées pour l'affichage
    return render_template('news_feed/news_feed.html', posts=posts)
