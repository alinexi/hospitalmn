from flask import Blueprint, render_template
from flask_login import login_required, current_user
from functools import wraps
from flask import abort

doctor_bp = Blueprint('doctor', __name__, url_prefix='/doctor')

def doctor_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or current_user.role.name not in ['chief_doctor', 'curing_doctor', 'consulting_doctor']:
            abort(403)
        return f(*args, **kwargs)
    return decorated_function

@doctor_bp.route('/dashboard')
@login_required
@doctor_required
def dashboard():
    """Doctor dashboard view."""
    return render_template('doctor/dashboard.html') 