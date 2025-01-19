# app/posts/routes.py

from flask import Blueprint, request, jsonify, render_template, redirect, url_for, flash, current_app
from flask_login import login_required, current_user
from datetime import datetime
import os
from werkzeug.utils import secure_filename

from app.models import Post, User
from app.extensions import db
from app.posts.forms import CreatePostForm

posts_bp = Blueprint('posts', __name__, template_folder='templates/posts')

@posts_bp.route('/create_post', methods=['GET', 'POST'])
@login_required
def create_post():
    """Version classique pour créer un post (séparée)."""
    form = CreatePostForm()
    if form.validate_on_submit():
        content_type = form.content_type.data
        title = form.title.data
        subtitle = form.subtitle.data
        content = form.content.data
        visibility = form.visibility.data

        image_file = form.image.data
        video_file = form.video.data
        music_file = form.music.data

        image_filename = None
        video_filename = None
        music_filename = None

        # Gérer l'upload
        if image_file:
            image_filename = secure_filename(image_file.filename)
            image_path = os.path.join(current_app.config['UPLOAD_FOLDER'], 'posts', 'images', image_filename)
            image_file.save(image_path)
            image_filename = f'posts/images/{image_filename}'

        if video_file:
            video_filename = secure_filename(video_file.filename)
            video_path = os.path.join(current_app.config['UPLOAD_FOLDER'], 'posts', 'videos', video_filename)
            video_file.save(video_path)
            video_filename = f'posts/videos/{video_filename}'

        if music_file:
            music_filename = secure_filename(music_file.filename)
            music_path = os.path.join(current_app.config['UPLOAD_FOLDER'], 'posts', 'music', music_filename)
            music_file.save(music_path)
            music_filename = f'posts/music/{music_filename}'

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

@posts_bp.route('/create_post_inline', methods=['POST'])
@login_required
def create_post_inline():
    """Création inline d'un post (ex. sur le profil)."""
    content_type = request.form.get('content_type', 'free')
    title = request.form.get('title', '')
    content = request.form.get('content', '')
    visibility = request.form.get('visibility', 'public')

    image_file = request.files.get('image')
    video_file = request.files.get('video')
    music_file = request.files.get('music')

    image_filename = None
    video_filename = None
    music_filename = None

    # Gérer upload image
    if image_file and image_file.filename:
        img_filename = secure_filename(image_file.filename)
        img_path = os.path.join(current_app.config['UPLOAD_FOLDER'], 'posts', 'images', img_filename)
        image_file.save(img_path)
        image_filename = f'posts/images/{img_filename}'

    if video_file and video_file.filename:
        vid_filename = secure_filename(video_file.filename)
        vid_path = os.path.join(current_app.config['UPLOAD_FOLDER'], 'posts', 'videos', vid_filename)
        video_file.save(vid_path)
        video_filename = f'posts/videos/{vid_filename}'

    if music_file and music_file.filename:
        mus_filename = secure_filename(music_file.filename)
        mus_path = os.path.join(current_app.config['UPLOAD_FOLDER'], 'posts', 'music', mus_filename)
        music_file.save(mus_path)
        music_filename = f'posts/music/{mus_filename}'

    new_post = Post(
        user_id=current_user.id,
        content_type=content_type,
        title=title,
        subtitle='',
        content=content,
        image=image_filename,
        video=video_filename,
        music=music_filename,
        visibility=visibility,
        created_at=datetime.utcnow()
    )
    db.session.add(new_post)
    db.session.commit()

    flash("Publication créée avec succès (inline).", "success")
    return redirect(url_for('profile.profile'))

@posts_bp.route('/delete_post/<int:post_id>', methods=['POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get(post_id)
    if not post or post.user_id != current_user.id:
        flash("Publication introuvable ou vous n'avez pas la permission.", "danger")
        return redirect(url_for('profile.profile'))

    try:
        db.session.delete(post)
        db.session.commit()
        flash("Publication supprimée avec succès.", "success")
    except:
        db.session.rollback()
        flash("Erreur lors de la suppression de la publication.", "danger")

    return redirect(url_for('profile.profile'))

@posts_bp.route('/news_feed', methods=['GET'])
@login_required
def news_feed():
    """Route alternative si vous ne voulez pas /news_feed/. 
       Mais on a aussi app/news_feed/routes.py. 
       On peut la laisser ou la retirer selon l'architecture."""
    # Exemple simplifié
    friends_ids = [f.id for f in current_user.friends]
    posts = Post.query.filter(
        (Post.user_id.in_(friends_ids)) | (Post.visibility == 'public')
    ).order_by(Post.created_at.desc()).all()

    return render_template('posts/news_feed.html', posts=posts)
