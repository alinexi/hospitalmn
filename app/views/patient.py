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

@patient_bp.route('/records', methods=['GET'])
@login_required
@patient_required
def view_records():
    # Logic to view patient records
    return render_template('patient/records.html')

@patient_bp.route('/appointments', methods=['GET', 'POST'])
@login_required
@patient_required
def manage_appointments():
    # Logic to request or cancel appointments
    return render_template('patient/appointments.html') 