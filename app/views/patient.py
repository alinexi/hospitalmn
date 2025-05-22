from flask import Blueprint, render_template, request, flash, redirect, url_for, abort
from flask_login import login_required, current_user
from app.models.user import User, Role
from app import db
from functools import wraps

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
    # Replace with actual query for patient's own records
    records = []
    return render_template('patient/records.html', records=records)

@patient_bp.route('/appointments', methods=['GET'])
@login_required
@patient_required
def manage_appointments():
    appointments = []  # Replace with actual query for patient's appointments
    return render_template('patient/appointments.html', appointments=appointments) 