from app import create_app, db
from app.models.user import User, Role
import os
from dotenv import load_dotenv
load_dotenv()
app = create_app()

with app.app_context():
    # Initialize roles
    Role.init_roles()

    # Create users for each role
    roles = ['sysadmin', 'receptionist', 'chief_doctor', 'curing_doctor', 'consulting_doctor', 'patient']
    for role_name in roles:
        role = Role.query.filter_by(name=role_name).first()
        if role:
            username = f'{role_name}_user'
            email = f'{role_name}@example.com'
            password = 'password123'  # Change this to a secure password in production

            user = User(
                username=username,
                email=email,
                first_name=f'{role_name.capitalize()}',
                last_name='User',
                phone='1234567890',
                role=role
            )
            user.password = password

            db.session.add(user)
            db.session.commit()

            print(f'Created user: {username} with password: {password}') 