from flask import Blueprint, render_template, request, flash, redirect, url_for, abort
from flask_login import login_required, current_user
from app.models.user import User, Role
from app import db
from functools import wraps

chief_doctor_bp = Blueprint('chief_doctor', __name__, url_prefix='/chief_doctor')

def chief_doctor_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or current_user.role.name != 'chief_doctor':
            abort(403)
        return f(*args, **kwargs)
    return decorated_function

@chief_doctor_bp.route('/medical_records', methods=['GET'])
@login_required
@chief_doctor_required
def view_medical_records():
    # Replace with actual query for all patient records
    medical_records = []
    return render_template('chief_doctor/medical_records.html', medical_records=medical_records)

@chief_doctor_bp.route('/assign_doctors', methods=['GET', 'POST'])
@login_required
@chief_doctor_required
def assign_doctors():
    if request.method == 'POST':
        patient_id = request.form['patient_id']
        doctor_id = request.form['doctor_id']
        # Logic to assign doctor to patient (replace with actual model logic)
        flash('Doctor assigned successfully.', 'success')
        return redirect(url_for('chief_doctor.assign_doctors'))
    return render_template('chief_doctor/assign_doctors.html')

@chief_doctor_bp.route('/audit_trail', methods=['GET'])
@login_required
@chief_doctor_required
def view_audit_trail():
    audit_trail = []  # Replace with actual query for audit logs
    return render_template('chief_doctor/audit_trail.html', audit_trail=audit_trail) 