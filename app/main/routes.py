
import os
from flask import Blueprint, render_template, jsonify, send_from_directory, current_app
from app.extensions import db

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    """Landing page with signup form."""
    return render_template('index.html')

@main_bp.app_errorhandler(404)
def not_found_error(error):
    return jsonify({"error": "Not found"}), 404

@main_bp.app_errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return jsonify({"error": "Internal server error"}), 500

@main_bp.route('/uploads/<path:filename>')
def uploaded_file(filename):
    return send_from_directory(current_app.config['UPLOAD_FOLDER'], filename)
