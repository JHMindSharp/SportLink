from flask import Blueprint, request, render_template, redirect, url_for, flash
from flask_login import login_required, current_user
from app.models import User, Message
from app.extensions import db

messages_bp = Blueprint('messages', __name__)

@messages_bp.route('/inbox', methods=['GET'])
@login_required
def inbox():
    messages = Message.query.filter_by(recipient_id=current_user.id).order_by(Message.timestamp.desc()).all()
    return render_template('messages/inbox.html', messages=messages)

@messages_bp.route('/send_message/<int:user_id>', methods=['GET', 'POST'])
@login_required
def send_message(user_id):
    recipient = User.query.get_or_404(user_id)
    if request.method == 'POST':
        body = request.form.get('body')
        new_message = Message(sender_id=current_user.id, recipient_id=recipient.id, body=body)
        db.session.add(new_message)
        db.session.commit()
        flash("Message envoyé avec succès.", "success")
        return redirect(url_for('messages.inbox'))

    return render_template('messages/send_message.html', recipient=recipient)
