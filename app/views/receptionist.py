from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify
from flask_login import login_required, current_user
from app.models.patient import Patient
from app.models.appointment import Appointment
from app.models.user import User, Role
from app import db
from functools import wraps
from datetime import datetime, timedelta
from sqlalchemy import or_

receptionist_bp = Blueprint('receptionist', __name__, url_prefix='/receptionist')

def receptionist_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or current_user.role.name != 'receptionist':
            flash('You do not have permission to access this page.', 'danger')
            return redirect(url_for('main.index'))
        return f(*args, **kwargs)
    return decorated_function

@receptionist_bp.route('/dashboard')
@login_required
@receptionist_required
def dashboard():
    """Receptionist dashboard view."""
    today = datetime.now().date()
    upcoming_appointments = Appointment.query.filter(
        Appointment.appointment_date >= today,
        Appointment.status == 'scheduled'
    ).order_by(Appointment.appointment_date).limit(5).all()
    
    return render_template('receptionist/dashboard.html', upcoming_appointments=upcoming_appointments)

# Patient Management
@receptionist_bp.route('/register_patient', methods=['GET', 'POST'])
@login_required
@receptionist_required
def register_patient():
    if request.method == 'POST':
        try:
            new_patient = Patient(
                first_name=request.form['first_name'],
                last_name=request.form['last_name'],
                date_of_birth=datetime.strptime(request.form['date_of_birth'], '%Y-%m-%d').date(),
                gender=request.form['gender'],
                phone=request.form['phone'],
                email=request.form['email'],
                address=request.form['address'],
                emergency_contact_name=request.form['emergency_contact_name'],
                emergency_contact_phone=request.form['emergency_contact_phone'],
                blood_type=request.form['blood_type'],
                allergies=request.form['allergies'],
                medical_history=request.form['medical_history']
            )
            db.session.add(new_patient)
            db.session.commit()
            flash('Patient registered successfully!', 'success')
            return redirect(url_for('receptionist.view_patient', patient_id=new_patient.id))
        except Exception as e:
            db.session.rollback()
            flash(f'Error registering patient: {str(e)}', 'danger')
    
    return render_template('receptionist/register_patient.html')

@receptionist_bp.route('/patients')
@login_required
@receptionist_required
def list_patients():
    search_query = request.args.get('search', '')
    page = request.args.get('page', 1, type=int)
    per_page = 10

    query = Patient.query
    if search_query:
        query = query.filter(or_(
            Patient.first_name.ilike(f'%{search_query}%'),
            Patient.last_name.ilike(f'%{search_query}%'),
            Patient.phone.ilike(f'%{search_query}%'),
            Patient.email.ilike(f'%{search_query}%')
        ))
    
    patients = query.order_by(Patient.last_name).paginate(page=page, per_page=per_page)
    return render_template('receptionist/patients.html', patients=patients, search_query=search_query)

@receptionist_bp.route('/patient/<int:patient_id>')
@login_required
@receptionist_required
def view_patient(patient_id):
    patient = Patient.query.get_or_404(patient_id)
    return render_template('receptionist/view_patient.html', patient=patient)

@receptionist_bp.route('/patient/<int:patient_id>/edit', methods=['GET', 'POST'])
@login_required
@receptionist_required
def edit_patient(patient_id):
    patient = Patient.query.get_or_404(patient_id)
    
    if request.method == 'POST':
        try:
            patient.first_name = request.form['first_name']
            patient.last_name = request.form['last_name']
            patient.phone = request.form['phone']
            patient.email = request.form['email']
            patient.address = request.form['address']
            patient.emergency_contact_name = request.form['emergency_contact_name']
            patient.emergency_contact_phone = request.form['emergency_contact_phone']
            patient.blood_type = request.form['blood_type']
            patient.allergies = request.form['allergies']
            patient.medical_history = request.form['medical_history']
            
            db.session.commit()
            flash('Patient information updated successfully!', 'success')
            return redirect(url_for('receptionist.view_patient', patient_id=patient.id))
        except Exception as e:
            db.session.rollback()
            flash(f'Error updating patient information: {str(e)}', 'danger')
    
    return render_template('receptionist/edit_patient.html', patient=patient)

# Appointment Management
@receptionist_bp.route('/appointments')
@login_required
@receptionist_required
def appointment_calendar():
    doctors = User.query.join(Role).filter(Role.name.in_(['chief_doctor', 'curing_doctor', 'consulting_doctor'])).all()
    return render_template('receptionist/appointment_calendar.html', doctors=doctors)

@receptionist_bp.route('/appointments/schedule', methods=['GET', 'POST'])
@login_required
@receptionist_required
def schedule_appointment():
    if request.method == 'POST':
        try:
            new_appointment = Appointment(
                patient_id=request.form['patient_id'],
                doctor_id=request.form['doctor_id'],
                appointment_date=datetime.strptime(
                    f"{request.form['appointment_date']} {request.form['appointment_time']}", 
                    '%Y-%m-%d %H:%M'
                ),
                duration=int(request.form['duration']),
                reason=request.form['reason'],
                notes=request.form.get('notes', '')
            )
            db.session.add(new_appointment)
            db.session.commit()
            flash('Appointment scheduled successfully!', 'success')
            return redirect(url_for('receptionist.appointment_calendar'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error scheduling appointment: {str(e)}', 'danger')

    patients = Patient.query.order_by(Patient.last_name).all()
    doctors = User.query.join(Role).filter(Role.name.in_(['chief_doctor', 'curing_doctor', 'consulting_doctor'])).all()
    return render_template('receptionist/schedule_appointment.html', patients=patients, doctors=doctors)

@receptionist_bp.route('/appointments/<int:appointment_id>/reschedule', methods=['POST'])
@login_required
@receptionist_required
def reschedule_appointment(appointment_id):
    appointment = Appointment.query.get_or_404(appointment_id)
    try:
        new_date = datetime.strptime(
            f"{request.form['appointment_date']} {request.form['appointment_time']}", 
            '%Y-%m-%d %H:%M'
        )
        appointment.appointment_date = new_date
        db.session.commit()
        flash('Appointment rescheduled successfully!', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error rescheduling appointment: {str(e)}', 'danger')
    return redirect(url_for('receptionist.appointment_calendar'))

@receptionist_bp.route('/appointments/<int:appointment_id>/cancel', methods=['POST'])
@login_required
@receptionist_required
def cancel_appointment(appointment_id):
    appointment = Appointment.query.get_or_404(appointment_id)
    try:
        appointment.status = 'cancelled'
        db.session.commit()
        flash('Appointment cancelled successfully!', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error cancelling appointment: {str(e)}', 'danger')
    return redirect(url_for('receptionist.appointment_calendar'))

@receptionist_bp.route('/api/appointments')
@login_required
@receptionist_required
def get_appointments():
    start_date = request.args.get('start', type=str)
    end_date = request.args.get('end', type=str)
    doctor_id = request.args.get('doctor_id', type=int)
    
    query = Appointment.query
    if start_date and end_date:
        query = query.filter(
            Appointment.appointment_date >= datetime.strptime(start_date, '%Y-%m-%d'),
            Appointment.appointment_date <= datetime.strptime(end_date, '%Y-%m-%d')
        )
    if doctor_id:
        query = query.filter(Appointment.doctor_id == doctor_id)
    
    appointments = query.all()
    events = []
    for appointment in appointments:
        events.append({
            'id': appointment.id,
            'title': f'{appointment.patient.first_name} {appointment.patient.last_name}',
            'start': appointment.appointment_date.isoformat(),
            'end': (appointment.appointment_date + timedelta(minutes=appointment.duration)).isoformat(),
            'status': appointment.status
        })
    return jsonify(events) 