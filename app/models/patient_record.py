from datetime import datetime
from app import db
from app.utils.crypto import encrypt_data, decrypt_data, sign_data, verify_signature

class PatientRecord(db.Model):
    """Encrypted patient medical records."""
    __tablename__ = 'patient_records'
    
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    doctor_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    # Encrypted fields
    _encrypted_diagnosis = db.Column('diagnosis', db.Text, nullable=False)
    _encrypted_treatment = db.Column('treatment', db.Text)
    _encrypted_notes = db.Column('notes', db.Text)
    
    # Digital signature
    signature = db.Column(db.Text, nullable=False)
    
    # Metadata
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    patient = db.relationship('User', foreign_keys=[patient_id], backref='medical_records')
    doctor = db.relationship('User', foreign_keys=[doctor_id], backref='created_records')
    
    @property
    def diagnosis(self):
        """Decrypt and return the diagnosis."""
        return decrypt_data(self._encrypted_diagnosis)
    
    @diagnosis.setter
    def diagnosis(self, value):
        """Encrypt and store the diagnosis."""
        self._encrypted_diagnosis = encrypt_data(value)
        self._update_signature()
    
    @property
    def treatment(self):
        """Decrypt and return the treatment."""
        return decrypt_data(self._encrypted_treatment) if self._encrypted_treatment else None
    
    @treatment.setter
    def treatment(self, value):
        """Encrypt and store the treatment."""
        self._encrypted_treatment = encrypt_data(value) if value else None
        self._update_signature()
    
    @property
    def notes(self):
        """Decrypt and return the notes."""
        return decrypt_data(self._encrypted_notes) if self._encrypted_notes else None
    
    @notes.setter
    def notes(self, value):
        """Encrypt and store the notes."""
        self._encrypted_notes = encrypt_data(value) if value else None
        self._update_signature()
    
    def _update_signature(self):
        """Update the digital signature for the record."""
        data_to_sign = f"{self._encrypted_diagnosis}{self._encrypted_treatment or ''}{self._encrypted_notes or ''}"
        self.signature = sign_data(data_to_sign)
    
    def verify_integrity(self):
        """Verify the digital signature of the record."""
        data_to_verify = f"{self._encrypted_diagnosis}{self._encrypted_treatment or ''}{self._encrypted_notes or ''}"
        return verify_signature(data_to_verify, self.signature)
    
    def __repr__(self):
        return f'<PatientRecord {self.id} for Patient {self.patient_id}>' 