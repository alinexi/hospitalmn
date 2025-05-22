from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from app import db, login_manager

class Role(db.Model):
    """User roles for access control."""
    __tablename__ = 'roles'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    description = db.Column(db.String(255))
    users = db.relationship('User', backref='role', lazy='dynamic')

    def __repr__(self):
        return f'<Role {self.name}>'

    @staticmethod
    def init_roles():
        roles = [
            {'name': 'sysadmin', 'description': 'System Administrator'},
            {'name': 'receptionist', 'description': 'Receptionist'},
            {'name': 'chief_doctor', 'description': 'Chief Doctor'},
            {'name': 'curing_doctor', 'description': 'Curing Doctor'},
            {'name': 'consulting_doctor', 'description': 'Consulting Doctor'},
            {'name': 'patient', 'description': 'Patient'}
        ]
        for role_data in roles:
            role = Role.query.filter_by(name=role_data['name']).first()
            if not role:
                role = Role(name=role_data['name'], description=role_data['description'])
                db.session.add(role)
        db.session.commit()

class User(UserMixin, db.Model):
    """User model for authentication and authorization."""
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'), nullable=False)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_login = db.Column(db.DateTime)
    
    # Profile information
    first_name = db.Column(db.String(64))
    last_name = db.Column(db.String(64))
    phone = db.Column(db.String(20))
    
    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)
        if self.role is None:
            self.role = Role.query.filter_by(name='patient').first()

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def has_role(self, role_name):
        return self.role.name == role_name

    def is_admin(self):
        return self.has_role('sysadmin')

    def is_doctor(self):
        return self.role.name in ['chiefdoctor', 'curingdoctor', 'consultingdoctor']

    def is_receptionist(self):
        return self.has_role('receptionist')

    def is_patient(self):
        return self.has_role('patient')

    def __repr__(self):
        return f'<User {self.username}>'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id)) 