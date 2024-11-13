from flask import Blueprint, request, jsonify, render_template, redirect, url_for, flash, current_app
from flask_login import login_required, current_user
from app.models import Post, User
from app.extensions import db
from werkzeug.utils import secure_filename
import os
from datetime import datetime
from app.posts.forms import CreatePostForm  # Import the form class
# Importation de la classe de formulaire

# Define the blueprint for handling routes related to posts and set the template folder
# Définition du blueprint pour gérer les routes liées aux publications et définir le dossier des modèles
posts_bp = Blueprint('posts', __name__, template_folder='templates/posts')

@posts_bp.route('/create_post', methods=['GET', 'POST'])
@login_required  # Ensure that only authenticated users can create posts
# S'assure que seuls les utilisateurs authentifiés peuvent créer des publications
def create_post():
    # Instantiate the form for creating a post
    # Instancie le formulaire pour créer une publication
    form = CreatePostForm()
    
    # Check if the form is submitted and valid
    # Vérifie si le formulaire est soumis et valide
    if form.validate_on_submit():
        content_type = form.content_type.data
        title = form.title.data
        subtitle = form.subtitle.data
        content = form.content.data
        visibility = form.visibility.data

        # Handle uploaded files (image, video, music)
        # Gestion des fichiers téléchargés (image, vidéo, musique)
        image_file = form.image.data
        video_file = form.video.data
        music_file = form.music.data

        image_filename = None
        video_filename = None
        music_filename = None

        # Save the uploaded image if present and set its path
        # Enregistre l'image téléchargée si présente et définit son chemin
        if image_file:
            image_filename = secure_filename(image_file.filename)
            image_path = os.path.join(current_app.config['UPLOAD_FOLDER'], 'posts', 'images', image_filename)
            image_file.save(image_path)
            image_filename = 'posts/images/' + image_filename

        # Save the uploaded video if present and set its path
        # Enregistre la vidéo téléchargée si présente et définit son chemin
        if video_file:
            video_filename = secure_filename(video_file.filename)
            video_path = os.path.join(current_app.config['UPLOAD_FOLDER'], 'posts', 'videos', video_filename)
            video_file.save(video_path)
            video_filename = 'posts/videos/' + video_filename

        # Save the uploaded music if present and set its path
        # Enregistre la musique téléchargée si présente et définit son chemin
        if music_file:
            music_filename = secure_filename(music_file.filename)
            music_path = os.path.join(current_app.config['UPLOAD_FOLDER'], 'posts', 'music', music_filename)
            music_file.save(music_path)
            music_filename = 'posts/music/' + music_filename

        # Create a new Post instance with provided data and save it to the database
        # Crée une nouvelle instance de Post avec les données fournies et l'enregistre dans la base de données
        new_post = Post(
            user_id=current_user.id,
            content_type=content_type,
            title=title,
            subtitle=subtitle,
            content=content,
            image=image_filename,
            video=video_filename,
            music=music_filename,
            visibility=visibility,
            created_at=datetime.utcnow()
        )
        db.session.add(new_post)
        db.session.commit()  # Commit the transaction to save the new post
        # Confirme la transaction pour enregistrer la nouvelle publication
        flash("Publication créée avec succès.", "success")
        return redirect(url_for('profile.profile'))

    # Render the template for creating a post and pass the form
    # Affiche le modèle pour créer une publication et passe le formulaire
    return render_template('posts/create_post.html', form=form)

@posts_bp.route('/delete_post/<int:post_id>', methods=['POST'])
@login_required  # Ensure that only authenticated users can delete posts
# S'assure que seuls les utilisateurs authentifiés peuvent supprimer des publications
def delete_post(post_id):
    # Retrieve the post by ID and check if the current user has permission to delete it
    # Récupère la publication par ID et vérifie si l'utilisateur actuel a la permission de la supprimer
    post = Post.query.get(post_id)
    if not post or post.user_id != current_user.id:
        flash("Publication introuvable ou vous n'avez pas la permission de la supprimer.", "danger")
        return redirect(url_for('profile.profile'))

    try:
        # Delete the post from the database
        # Supprime la publication de la base de données
        db.session.delete(post)
        db.session.commit()
        flash("Publication supprimée avec succès.", "success")
    except:
        # Roll back the transaction in case of an error
        # Annule la transaction en cas d'erreur
        db.session.rollback()
        flash("Une erreur est survenue lors de la suppression de la publication.", "danger")

    return redirect(url_for('profile.profile'))

@posts_bp.route('/news_feed', methods=['GET'])
@login_required  # Ensure that only authenticated users can view the news feed
# S'assure que seuls les utilisateurs authentifiés peuvent voir le fil d'actualité
def news_feed():
    # Retrieve the IDs of the current user's friends
    # Récupère les IDs des amis de l'utilisateur courant
    friends_ids = [friend.id for friend in current_user.friends]

    # Query the database for posts that are public or belong to friends
    # Interroge la base de données pour obtenir les publications publiques ou celles des amis
    posts = Post.query.filter(
        (Post.user_id.in_(friends_ids)) |
        (Post.visibility == 'public')
    ).order_by(Post.created_at.desc()).all()

    # Render the news feed template and pass the retrieved posts
    # Affiche le modèle du fil d'actualité et passe les publications récupérées
    return render_template('posts/news_feed.html', posts=posts)
