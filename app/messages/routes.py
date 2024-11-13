from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from app.models import Message, User
from app.extensions import db

# Define the blueprint for handling message-related routes and templates
# Définition du blueprint pour gérer les routes et modèles liés aux messages
messages_bp = Blueprint('messages', __name__, template_folder='templates/messages')

@messages_bp.route('/inbox', methods=['GET'])
@login_required  # Ensure that only authenticated users can access the inbox
# S'assure que seuls les utilisateurs authentifiés peuvent accéder à la boîte de réception
def inbox():
    # Query the database for messages received by the current user, ordered by timestamp (newest first)
    # Interroge la base de données pour obtenir les messages reçus par l'utilisateur actuel, triés par horodatage (du plus récent au plus ancien)
    messages = Message.query.filter_by(recipient_id=current_user.id).order_by(Message.timestamp.desc()).all()
    
    # Render the inbox template and pass the retrieved messages for display
    # Rendu du modèle de boîte de réception et passage des messages récupérés pour l'affichage
    return render_template('messages/inbox.html', messages=messages)

@messages_bp.route('/send_message/<int:user_id>', methods=['GET', 'POST'])
@login_required  # Ensure that only authenticated users can send messages
# S'assure que seuls les utilisateurs authentifiés peuvent envoyer des messages
def send_message(user_id):
    # Retrieve the recipient user from the database or return a 404 error if not found
    # Récupère l'utilisateur destinataire de la base de données ou renvoie une erreur 404 s'il n'est pas trouvé
    recipient = User.query.get_or_404(user_id)
    
    # Check if the request method is POST, indicating form submission
    # Vérifie si la méthode de requête est POST, indiquant la soumission du formulaire
    if request.method == 'POST':
        # Get the message body from the form input
        # Récupère le contenu du message depuis le formulaire
        body = request.form.get('body')
        
        # Check if the message body is empty and display an error message if so
        # Vérifie si le contenu du message est vide et affiche un message d'erreur dans ce cas
        if not body:
            flash("Le message ne peut pas être vide.", "danger")
            return redirect(url_for('messages.send_message', user_id=user_id))
        
        # Create a new Message object and add it to the database session
        # Crée un nouvel objet Message et l'ajoute à la session de la base de données
        message = Message(sender_id=current_user.id, recipient_id=recipient.id, body=body)
        db.session.add(message)
        db.session.commit()  # Commit the transaction to save the message
        # Confirme la transaction pour enregistrer le message
        
        # Display a success message and redirect the user to their inbox
        # Affiche un message de succès et redirige l'utilisateur vers sa boîte de réception
        flash("Message envoyé avec succès.", "success")
        return redirect(url_for('messages.inbox'))
    
    # Render the send message template and pass the recipient information for display
    # Rendu du modèle d'envoi de message et passage des informations du destinataire pour l'affichage
    return render_template('messages/send_message.html', recipient=recipient)
