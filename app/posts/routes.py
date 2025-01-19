# app/posts/routes.py

"""
app/posts/routes.py

Ce module définit les routes liées à la gestion des publications (posts)
dans l'application SportLink. Il inclut les fonctionnalités de création
et de suppression de publications, tandis que l'affichage global
du fil d'actualité est géré dans app/news_feed/routes.py.
"""

from flask import Blueprint, request, jsonify, render_template, redirect, url_for, flash, current_app
from flask_login import login_required, current_user
from app.models import Post, User
from app.extensions import db
from werkzeug.utils import secure_filename
import os
from datetime import datetime
from app.posts.forms import CreatePostForm

# Définition du Blueprint pour les routes liées aux posts
posts_bp = Blueprint('posts', __name__, template_folder='templates/posts')


@posts_bp.route('/create_post', methods=['GET', 'POST'])
@login_required
def create_post():
    """
    Gère la création d'une nouvelle publication.

    GET:
      - Affiche le formulaire de création de post (CreatePostForm).
    
    POST:
      - Valide la soumission du formulaire.
      - Traite les fichiers uploadés (image, vidéo, musique) et les enregistre.
      - Crée une nouvelle entrée Post dans la base de données.
      - Redirige vers la page de profil de l'utilisateur en cas de succès.
    """
    form = CreatePostForm()
    if form.validate_on_submit():
        content_type = form.content_type.data
        title = form.title.data
        subtitle = form.subtitle.data
        content = form.content.data
        visibility = form.visibility.data

        # Gestion des fichiers uploadés
        image_file = form.image.data
        video_file = form.video.data
        music_file = form.music.data

        image_filename = None
        video_filename = None
        music_filename = None

        if image_file:
            image_filename = secure_filename(image_file.filename)
            image_path = os.path.join(current_app.config['UPLOAD_FOLDER'], 'posts', 'images', image_filename)
            image_file.save(image_path)
            image_filename = 'posts/images/' + image_filename

        if video_file:
            video_filename = secure_filename(video_file.filename)
            video_path = os.path.join(current_app.config['UPLOAD_FOLDER'], 'posts', 'videos', video_filename)
            video_file.save(video_path)
            video_filename = 'posts/videos/' + video_filename

        if music_file:
            music_filename = secure_filename(music_file.filename)
            music_path = os.path.join(current_app.config['UPLOAD_FOLDER'], 'posts', 'music', music_filename)
            music_file.save(music_path)
            music_filename = 'posts/music/' + music_filename

        # Création de l'objet Post
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
        db.session.commit()
        flash("Publication créée avec succès.", "success")
        return redirect(url_for('profile.profile'))

    return render_template('posts/create_post.html', form=form)


@posts_bp.route('/delete_post/<int:post_id>', methods=['POST'])
@login_required
def delete_post(post_id):
    """
    Gère la suppression d'un post par son auteur.

    - Vérifie que le post existe et qu'il appartient bien à l'utilisateur connecté.
    - Supprime le post de la base de données.
    - Redirige vers la page de profil de l'utilisateur, avec un message de succès ou d'erreur.
    """
    post = Post.query.get(post_id)
    if not post or post.user_id != current_user.id:
        flash("Publication introuvable ou vous n'avez pas la permission de la supprimer.", "danger")
        return redirect(url_for('profile.profile'))

    try:
        db.session.delete(post)
        db.session.commit()
        flash("Publication supprimée avec succès.", "success")
    except:
        db.session.rollback()
        flash("Une erreur est survenue lors de la suppression de la publication.", "danger")

    return redirect(url_for('profile.profile'))

# -----------------------------------------------------------
# NOTE : la route news_feed a été supprimée d'ici car
# elle est désormais gérée dans app/news_feed/routes.py
# -----------------------------------------------------------
