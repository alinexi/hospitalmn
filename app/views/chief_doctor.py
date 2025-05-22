@chief_doctor_bp.route('/medical_records', methods=['GET'])
@login_required
@chief_doctor_required
def view_medical_records():
    # Logic to view all patients' medical records
    return render_template('chief_doctor/medical_records.html')

@chief_doctor_bp.route('/assign_doctors', methods=['GET', 'POST'])
@login_required
@chief_doctor_required
def assign_doctors():
    # Logic to assign or reassign Curing Doctors
    return render_template('chief_doctor/assign_doctors.html')

@chief_doctor_bp.route('/audit_trail', methods=['GET'])
@login_required
@chief_doctor_required
def view_audit_trail():
    # Logic to view audit trail
    return render_template('chief_doctor/audit_trail.html') 