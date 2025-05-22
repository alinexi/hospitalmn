from flask import Blueprint, render_template
from flask_login import login_required, current_user

receptionist_bp = Blueprint('receptionist', __name__, url_prefix='/receptionist')

@receptionist_bp.route('/dashboard')
@login_required
def dashboard():
    """Receptionist dashboard view."""
    if not current_user.is_receptionist():
        return render_template('errors/403.html'), 403
    return render_template('receptionist/dashboard.html') 