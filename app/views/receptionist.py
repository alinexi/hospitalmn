from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from app.models.user import User, Role
from app import db
from functools import wraps
from flask import abort

receptionist_bp = Blueprint('receptionist', __name__, url_prefix='/receptionist')

def receptionist_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or current_user.role.name != 'receptionist':
            abort(403)
        return f(*args, **kwargs)
    return decorated_function

@receptionist_bp.route('/dashboard')
@login_required
@receptionist_required
def dashboard():
    """Receptionist dashboard view."""
    return render_template('receptionist/dashboard.html')

@receptionist_bp.route('/register_patient', methods=['GET', 'POST'])
@login_required
@receptionist_required
def register_patient():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        phone = request.form['phone']
        role = Role.query.filter_by(name='patient').first()
        password = 'patient123'  # Default password, should be changed by patient
        user = User(username=username, email=email, first_name=first_name, last_name=last_name, phone=phone, role=role)
        user.password = password
        db.session.add(user)
        db.session.commit()
        flash('Patient registered successfully.', 'success')
        return redirect(url_for('receptionist.register_patient'))
    return render_template('receptionist/register_patient.html')

@receptionist_bp.route('/appointments', methods=['GET'])
@login_required
@receptionist_required
def view_appointments():
    appointments = []  # Replace with actual query
    return render_template('receptionist/appointments.html', appointments=appointments)

@receptionist_bp.route('/patient_info', methods=['GET'])
@login_required
@receptionist_required
def lookup_patient_info():
    patient = None
    if 'patient_id' in request.args:
        patient = User.query.filter_by(id=request.args['patient_id'], role=Role.query.filter_by(name='patient').first()).first()
    return render_template('receptionist/patient_info.html', patient=patient) 