@curing_doctor_bp.route('/patient_records', methods=['GET'])
@login_required
@curing_doctor_required
def view_patient_records():
    # Logic to view patient records
    return render_template('curing_doctor/patient_records.html')

@curing_doctor_bp.route('/grant_access', methods=['GET', 'POST'])
@login_required
@curing_doctor_required
def grant_access():
    # Logic to grant Consulting Doctor access
    return render_template('curing_doctor/grant_access.html')

@curing_doctor_bp.route('/appointments', methods=['GET'])
@login_required
@curing_doctor_required
def view_appointments():
    # Logic to view appointments
    return render_template('curing_doctor/appointments.html') 