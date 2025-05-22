@consulting_doctor_bp.route('/patient_records', methods=['GET'])
@login_required
@consulting_doctor_required
def view_patient_records():
    # Logic to view patient records
    return render_template('consulting_doctor/patient_records.html')

@consulting_doctor_bp.route('/add_notes', methods=['GET', 'POST'])
@login_required
@consulting_doctor_required
def add_consultation_notes():
    # Logic to add consultation notes
    return render_template('consulting_doctor/add_notes.html') 