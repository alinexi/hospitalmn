from flask import Blueprint, render_template, request, flash, redirect, url_for, abort
from flask_login import login_required, current_user
from app.models.user import User, Role
from app import db
from functools import wraps

curing_doctor_bp = Blueprint('curing_doctor', __name__, url_prefix='/curing_doctor')

def curing_doctor_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or current_user.role.name != 'curing_doctor':
            abort(403)
        return f(*args, **kwargs)
    return decorated_function

@curing_doctor_bp.route('/patient_records', methods=['GET'])
@login_required
@curing_doctor_required
def view_patient_records():
    # Replace with actual query for patient records assigned to this doctor
    patient_records = []
    return render_template('curing_doctor/patient_records.html', patient_records=patient_records)

@curing_doctor_bp.route('/grant_access', methods=['GET', 'POST'])
@login_required
@curing_doctor_required
def grant_access():
    if request.method == 'POST':
        patient_id = request.form['patient_id']
        consulting_doctor_id = request.form['consulting_doctor_id']
        # Logic to grant access to Consulting Doctor (replace with actual model logic)
        flash('Access granted successfully.', 'success')
        return redirect(url_for('curing_doctor.grant_access'))
    return render_template('curing_doctor/grant_access.html')

@curing_doctor_bp.route('/appointments', methods=['GET'])
@login_required
@curing_doctor_required
def manage_appointments():
    appointments = []  # Replace with actual query for appointments
    return render_template('curing_doctor/appointments.html', appointments=appointments) 