import click
from flask.cli import with_appcontext
from app import db
from app.models.user import User, Role
from app.utils.crypto import generate_keys

@click.command('init-db')
@with_appcontext
def init_db_command():
    """Initialize the database with roles and admin user."""
    # Create roles
    roles = [
        ('sysadmin', 'System Administrator'),
        ('receptionist', 'Receptionist'),
        ('chiefdoctor', 'Chief Doctor'),
        ('curingdoctor', 'Curing Doctor'),
        ('consultingdoctor', 'Consulting Doctor'),
        ('patient', 'Patient')
    ]
    
    for name, description in roles:
        role = Role.query.filter_by(name=name).first()
        if role is None:
            role = Role(name=name, description=description)
            db.session.add(role)
    
    # Create admin user if not exists
    admin_role = Role.query.filter_by(name='sysadmin').first()
    admin = User.query.filter_by(username='admin').first()
    if admin is None:
        admin = User(
            username='admin',
            email='admin@hospital.com',
            first_name='System',
            last_name='Administrator',
            role=admin_role
        )
        admin.password = 'admin123'  # Change this in production!
        db.session.add(admin)
    
    db.session.commit()
    click.echo('Initialized the database.')

@click.command('generate-keys')
@with_appcontext
def generate_keys_command():
    """Generate new encryption keys."""
    try:
        generate_keys()
        click.echo('Generated new encryption keys.')
    except Exception as e:
        click.echo(f'Error generating keys: {str(e)}', err=True)

def init_app(app):
    """Register CLI commands."""
    app.cli.add_command(init_db_command)
    app.cli.add_command(generate_keys_command) 