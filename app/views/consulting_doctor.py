from flask import Blueprint, render_template, request, flash, redirect, url_for, abort
from flask_login import login_required, current_user
from app.models.user import User, Role
from app import db
from functools import wraps

consulting_doctor_bp = Blueprint('consulting_doctor', __name__, url_prefix='/consulting_doctor')

def consulting_doctor_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or current_user.role.name != 'consulting_doctor':
            abort(403)
        return f(*args, **kwargs)
    return decorated_function

@consulting_doctor_bp.route('/patient_records', methods=['GET'])
@login_required
@consulting_doctor_required
def view_patient_records():
    # Replace with actual query for patient records accessible to this doctor
    patient_records = []
    return render_template('consulting_doctor/patient_records.html', patient_records=patient_records)

@consulting_doctor_bp.route('/add_notes', methods=['GET', 'POST'])
@login_required
@consulting_doctor_required
def add_notes():
    if request.method == 'POST':
        patient_id = request.form['patient_id']
        notes = request.form['notes']
        # Logic to add consultation notes (replace with actual model logic)
        flash('Notes added successfully.', 'success')
        return redirect(url_for('consulting_doctor.add_notes'))
    return render_template('consulting_doctor/add_notes.html') 