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

@receptionist_bp.route('/register_patient', methods=['GET', 'POST'])
@login_required
@receptionist_required
def register_patient():
    # Logic to register new patients
    return render_template('receptionist/register_patient.html')

@receptionist_bp.route('/appointments', methods=['GET'])
@login_required
@receptionist_required
def view_appointments():
    # Logic to view appointments
    return render_template('receptionist/appointments.html')

@receptionist_bp.route('/patient_info', methods=['GET'])
@login_required
@receptionist_required
def lookup_patient_info():
    # Logic to lookup patient info
    return render_template('receptionist/patient_info.html') 