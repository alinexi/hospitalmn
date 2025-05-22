from flask import Blueprint, render_template
from flask_login import login_required, current_user
from functools import wraps
from flask import abort

patient_bp = Blueprint('patient', __name__, url_prefix='/patient')

def patient_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or current_user.role.name != 'patient':
            abort(403)
        return f(*args, **kwargs)
    return decorated_function

@patient_bp.route('/dashboard')
@login_required
@patient_required
def dashboard():
    """Patient dashboard view."""
    return render_template('patient/dashboard.html') 