from flask import Blueprint, request, jsonify, render_template, redirect, url_for, flash, current_app
from flask_login import login_user, logout_user, login_required
from app.models import User
from app.extensions import db, bcrypt, mail
from itsdangerous import URLSafeTimedSerializer
from flask_mail import Message
from datetime import datetime
from flask_dance.contrib.facebook import facebook
from flask_dance.contrib.strava import strava
from app.auth.utils import register_user_if_new

auth_bp = Blueprint('auth', __name__)
bp = Blueprint('main', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    try:
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        profile_image = None

        if not username or not email or not password:
            flash("Nom d'utilisateur, email et mot de passe sont obligatoires.", "danger")
            return redirect(url_for('auth.register'))

        # Vérification de l'existence de l'utilisateur
        if User.query.filter_by(username=username).first() or User.query.filter_by(email=email).first():
            flash("Nom d'utilisateur ou email déjà existant.", "danger")
            return redirect(url_for('auth.register'))

        user = User(username=username, email=email)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        send_confirmation_email(user.email)
        
        flash("Inscription réussie ! Vérifiez votre email pour confirmer votre inscription.", "success")
        return redirect(url_for('auth.login'))

    except Exception as e:
        return jsonify({"error": "Erreur interne"}), 500


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        user = User.query.filter_by(username=username).first()
        if user is None or not user.check_password(password):
            flash("Nom d'utilisateur ou mot de passe invalide.", "danger")
            return redirect(url_for('auth.login'))

        login_user(user)
        flash("Connexion réussie.", "success")
        next_page = request.args.get('next')
        return redirect(next_page or url_for('profile.edit_profile'))
    
    return render_template('auth/login.html')

@auth_bp.route('/facebook_login')
def facebook_login():
    if not facebook.authorized:
        return redirect(url_for("facebook.login"))

    resp = facebook.get("/me?fields=id,name,email")
    if resp.ok:
        user_data = resp.json()
        user = register_user_if_new(
            provider="facebook",
            provider_id=user_data["id"],
            email=user_data.get("email"),
            username=user_data["name"]
        )
        login_user(user)
        flash("Connexion réussie avec Facebook.", "success")
        return redirect(url_for("profile.edit_profile"))
    flash("Échec de connexion via Facebook.", "danger")
    return redirect(url_for("auth.login"))

@auth_bp.route('/strava_login')
def strava_login():
    if not strava.authorized:
        return redirect(url_for("strava.login"))

    # Récupérer les données utilisateur de Strava
    resp = strava.get("/athlete")
    if resp.ok:
        user_data = resp.json()
        
        # Récupérer les informations de base
        provider_id = user_data.get("id")
        email = user_data.get("email")
        username = user_data.get("username") or f"strava_{provider_id}"

        # Vérifier si l'utilisateur existe déjà
        user = User.query.filter_by(provider_id=provider_id, provider="strava").first()
        if not user:
            # Créer un nouvel utilisateur si non existant
            user = User(
                provider="strava",
                provider_id=provider_id,
                email=email,
                username=username
            )
            db.session.add(user)
            db.session.commit()
            flash("Utilisateur créé avec succès via Strava.", "success")
        
        # Connecter l'utilisateur
        login_user(user)
        flash("Connexion réussie avec Strava.", "success")
        
        # Rediriger vers la page de création de profil
        return redirect(url_for("profile.edit_profile"))

    flash("Échec de connexion via Strava.", "danger")
    return redirect(url_for("auth.login"))

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash("Vous avez été déconnecté.", "info")
    return redirect(url_for('main.index'))

def send_confirmation_email(user_email):
    s = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
    token = s.dumps(user_email, salt='email-confirm-salt')
    confirm_url = url_for('auth.confirm_email', token=token, _external=True)
    html = render_template('confirm_email.html', confirm_url=confirm_url)
    send_email('Please confirm your email', [user_email], html)

@auth_bp.route('/confirm/<token>')
def confirm_email(token):
    s = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
    try:
        email = s.loads(token, salt='email-confirm-salt', max_age=3600)
    except Exception:
        flash("Le lien de confirmation est invalide ou a expiré.", "danger")
        return redirect(url_for('main.index'))

    user = User.query.filter_by(email=email).first_or_404()
    user.email_confirmed = True
    db.session.commit()
    flash("Votre email a été confirmé ! Vous pouvez maintenant vous connecter.", "success")
    return redirect(url_for('main.index'))

def send_email(subject, recipients, html_body):
    msg = Message(subject, recipients=recipients)
    msg.html = html_body
    mail.send(msg)
