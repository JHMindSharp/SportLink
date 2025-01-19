# app/news_feed/routes.py

"""
app/news_feed/routes.py

Ce module définit les routes liées à la fonctionnalité de fil d'actualité
dans l'application SportLink. Il permet à l'utilisateur connecté de
voir les publications pertinentes (les siennes, celles de ses amis,
ainsi que tout post déclaré 'public').
"""

from flask import Blueprint, render_template, request
from flask_login import login_required, current_user
from app.models import Post
from app.extensions import db

# Définition du Blueprint pour les routes du fil d'actualité
news_feed_bp = Blueprint('news_feed', __name__, template_folder='templates/news_feed')

@news_feed_bp.route('/', methods=['GET'])
@login_required
def news_feed():
    """
    Affiche le fil d'actualité pour l'utilisateur connecté.

    Logique adoptée pour la visibilité des posts :
    1. Les publications créées par l'utilisateur (sans tenir compte de la visibilité).
    2. Les publications de ses amis (quelle que soit leur visibilité *ou* seulement public, 
       selon votre logique).
    3. Toutes les publications marquées 'public' (donc accessibles à tous).

    Remarque :
    - Si vous voulez que l'utilisateur ne voie que les posts "public" de ses amis (mais pas 
      leurs posts "private"), il suffit d'ajuster le filtre.

    Retourne :
    - Le template 'news_feed.html' avec la liste des posts à afficher.
    """
    # Récupérer la liste des IDs d'amis
    friends_ids = [friend.id for friend in current_user.friends]

    # Inclure l'ID du user courant pour afficher ses propres posts
    friends_ids.append(current_user.id)

    # Ici, on fusionne la logique de "posts/routes.py" et "news_feed/routes.py" 
    # pour n'avoir qu'une seule route de fil d'actualité.

    # On veut récupérer tous les posts qui proviennent de l'utilisateur courant 
    # ou de ses amis, + tous les posts 'public' de n'importe qui.
    # => Condition : (user_id dans friends_ids) OU (visibility == 'public')
    posts = Post.query.filter(
        (Post.user_id.in_(friends_ids)) | (Post.visibility == 'public')
    ).order_by(Post.created_at.desc()).all()

    # Rendre le template avec la liste des posts
    return render_template('news_feed/news_feed.html', posts=posts)
