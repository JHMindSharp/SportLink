"""
app/posts/routes.py

This module defines routes related to managing posts in the SportLink application.
It includes features for creating, deleting, and viewing posts in the news feed.

Components:
- `create_post`: Allows users to create a new post with multimedia and visibility settings.
- `delete_post`: Allows users to delete their own posts.
- `news_feed`: Displays posts from friends and public posts in a news feed format.
"""

from flask import Blueprint, request, jsonify, render_template, redirect, url_for, flash, current_app
from flask_login import login_required, current_user
from app.models import Post, User
from app.extensions import db
from werkzeug.utils import secure_filename
import os
from datetime import datetime
from app.posts.forms import CreatePostForm  # Import du formulaire

# Define the Blueprint for post-related routes
posts_bp = Blueprint('posts', __name__, template_folder='templates/posts')

@posts_bp.route('/create_post', methods=['GET', 'POST'])
@login_required
def create_post():
    """
    Handles the creation of a new post.

    GET:
    - Renders the post creation form.

    POST:
    - Validates the form submission.
    - Processes uploaded files (image, video, music) and saves them.
    - Creates a new post in the database with the provided details.

    Returns:
    - Redirects to the user's profile after successful post creation.
    - Renders the 'create_post.html' template on form validation failure.
    """
    form = CreatePostForm()
    if form.validate_on_submit():
        content_type = form.content_type.data
        title = form.title.data
        subtitle = form.subtitle.data
        content = form.content.data
        visibility = form.visibility.data

        # Handle uploaded files
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

        # Create a new post
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
    Handles the deletion of a user's post.

    - Checks if the post exists and belongs to the current user.
    - Deletes the post from the database.

    Parameters:
    - `post_id`: ID of the post to be deleted.

    Returns:
    - Redirects to the user's profile after successful deletion.
    - Displays an error message if the post cannot be deleted.
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

@posts_bp.route('/news_feed', methods=['GET'])
@login_required
def news_feed():
    """
    Displays the news feed for the current user.

    - Retrieves posts from the user's friends and public posts.
    - Orders posts by their creation date in descending order.

    Returns:
    - Rendered 'news_feed.html' template with the list of posts.
    """
    # Get IDs of the current user's friends
    friends_ids = [friend.id for friend in current_user.friends]

    # Query the database for posts from friends and public posts
    posts = Post.query.filter(
        (Post.user_id.in_(friends_ids)) |
        (Post.visibility == 'public')
    ).order_by(Post.created_at.desc()).all()

    # Render the news feed template with the retrieved posts
    return render_template('posts/news_feed.html', posts=posts)
