from flask import Blueprint, request, render_template, redirect, url_for, flash, current_app
from flask_login import login_user, logout_user, login_required, current_user
from app.models import User
from app.extensions import db, mail
from itsdangerous import URLSafeTimedSerializer
from flask_mail import Message
from app.auth.forms import RegistrationForm, LoginForm, ResetPasswordRequestForm, ResetPasswordForm
from flask_dance.contrib.strava import strava
from flask_dance.contrib.facebook import facebook

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/oauth_strava')
def oauth_strava():
    if not strava.authorized:
        flash('L\'autorisation avec Strava a échoué.', 'danger')
        return redirect(url_for('auth.login'))

    resp = strava.get('/athlete')
    if not resp.ok:
        flash('Impossible de récupérer les informations depuis Strava.', 'danger')
        return redirect(url_for('auth.login'))

    info = resp.json()
    email = info.get('email')
    first_name = info.get('firstname')
    last_name = info.get('lastname')

    if not email:
        flash('Votre compte Strava ne fournit pas d\'adresse email.', 'danger')
        return redirect(url_for('auth.login'))

    user = User.query.filter_by(email=email).first()
    if not user:
        # Créer un nouvel utilisateur
        user = User(
            email=email,
            username=f"{first_name}_{last_name}_{strava_id}",
            first_name=first_name,
            last_name=last_name,
            # Remplissez les autres champs requis avec des valeurs par défaut si nécessaire
        )
        db.session.add(user)
        db.session.commit()
        new_user = True
    else:
        new_user = False

    login_user(user)
    if new_user:
        flash('Inscription réussie via Strava !', 'success')
        return redirect(url_for('profile.complete_profile'))
    else:
        flash('Connexion réussie via Strava.', 'success')
        return redirect(url_for('profile.profile'))

@auth_bp.route('/oauth_facebook')
def oauth_facebook():
    if not facebook.authorized:
        flash('L\'autorisation avec Facebook a échoué.', 'danger')
        return redirect(url_for('auth.login'))

    resp = facebook.get('/me?fields=id,name,email,first_name,last_name')
    if not resp.ok:
        flash('Impossible de récupérer les informations depuis Facebook.', 'danger')
        return redirect(url_for('auth.login'))

    info = resp.json()
    email = info.get('email')
    first_name = info.get('first_name')
    last_name = info.get('last_name')

    if not email:
        flash('Votre compte Facebook ne fournit pas d\'adresse email.', 'danger')
        return redirect(url_for('auth.login'))

    user = User.query.filter_by(email=email).first()
    if not user:
        # Créer un nouvel utilisateur
        user = User(
            email=email,
            username=f"{first_name}_{last_name}_{facebook_id}",
            first_name=first_name,
            last_name=last_name,
            # Remplissez les autres champs requis avec des valeurs par défaut si nécessaire
        )
        db.session.add(user)
        db.session.commit()
        new_user = True
    else:
        new_user = False

    login_user(user)
    if new_user:
        flash('Inscription réussie via Facebook !', 'success')
        return redirect(url_for('profile.complete_profile'))
    else:
        flash('Connexion réussie via Facebook.', 'success')
        return redirect(url_for('profile.profile'))

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('profile.profile'))
    form = RegistrationForm()
    login_form = LoginForm()
    if form.validate_on_submit():
        user = User(
            username=form.username.data,
            email=form.email.data,
            first_name=form.first_name.data,
            last_name=form.last_name.data,
            birth_date=form.birth_date.data,
            gender=form.gender.data
        )
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        send_confirmation_email(user.email)
        flash("Inscription réussie ! Vérifiez votre email pour confirmer votre inscription.", "success")
        login_user(user)
        return redirect(url_for('profile.profile'))
    return render_template('auth/register.html', form=form, login_form=login_form, register_form=form)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('profile.profile'))
    form = LoginForm()
    register_form = RegistrationForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data

        user = User.query.filter_by(email=email).first()
        if user is None or not user.check_password(password):
            flash("Email ou mot de passe invalide.", "danger")
            return redirect(url_for('auth.login'))

        login_user(user)
        flash("Connexion réussie.", "success")
        next_page = request.args.get('next')
        return redirect(next_page or url_for('profile.profile'))
    return render_template('auth/login.html', form=form, register_form=register_form, login_form=form)

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
    html = render_template('auth/confirm_email.html', confirm_url=confirm_url)
    send_email('Veuillez confirmer votre email', [user_email], html)

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
    flash("Votre email a été confirmé !", "success")
    return redirect(url_for('profile.profile'))

def send_email(subject, recipients, html_body):
    msg = Message(subject, recipients=recipients)
    msg.html = html_body
    mail.send(msg)

@auth_bp.route('/reset_password_request', methods=['GET', 'POST'])
def reset_password_request():
    if current_user.is_authenticated:
        return redirect(url_for('profile.profile'))
    form = ResetPasswordRequestForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            send_password_reset_email(user)
        flash('Un email avec les instructions pour réinitialiser votre mot de passe a été envoyé.', 'info')
        return redirect(url_for('auth.login'))
    return render_template('auth/reset_password_request.html', form=form)

@auth_bp.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    if current_user.is_authenticated:
        return redirect(url_for('profile.profile'))
    s = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
    try:
        email = s.loads(token, salt='password-reset-salt', max_age=3600)
    except Exception:
        flash('Le lien de réinitialisation est invalide ou a expiré.', 'danger')
        return redirect(url_for('auth.reset_password_request'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=email).first_or_404()
        user.set_password(form.password.data)
        db.session.commit()
        flash('Votre mot de passe a été mis à jour.', 'success')
        return redirect(url_for('auth.login'))
    return render_template('auth/reset_password.html', form=form)
