from flask import Blueprint, render_template, request, flash, redirect, url_for, abort
from flask_login import login_required, current_user
from app.models.user import User, Role
from app import db
from functools import wraps
import json
import os
from werkzeug.security import generate_password_hash
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SelectField, validators

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or current_user.role.name != 'sysadmin':
            abort(403)
        return f(*args, **kwargs)
    return decorated_function

@admin_bp.route('/dashboard')
@login_required
@admin_required
def dashboard():
    """Admin dashboard view."""
    return render_template('admin/dashboard.html')

@admin_bp.route('/users', methods=['GET'])
@login_required
@admin_required
def manage_users():
    users = User.query.all()
    return render_template('admin/users.html', users=users)

@admin_bp.route('/settings', methods=['GET', 'POST'])
@login_required
@admin_required
def system_settings():
    settings = {}
    if os.path.exists('system_settings.json'):
        with open('system_settings.json', 'r') as f:
            settings = json.load(f)
    if request.method == 'POST':
        settings['password_policy'] = request.form['password_policy']
        with open('system_settings.json', 'w') as f:
            json.dump(settings, f)
        flash('Settings updated successfully.', 'success')
    return render_template('admin/settings.html', settings=settings)

@admin_bp.route('/audit-logs', methods=['GET'], endpoint='view_audit_logs')
@login_required
@admin_required
def view_audit_logs():
    # Example: Fetch audit logs from a table called AuditLog
    audit_logs = []
    if hasattr(db.Model, 'AuditLog'):
        audit_logs = db.session.query(db.Model.AuditLog).all()
    return render_template('admin/audit_logs.html', audit_logs=audit_logs)

@admin_bp.route('/edit_user/<int:user_id>', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_user(user_id):
    user = User.query.get_or_404(user_id)
    roles = Role.query.all()
    if request.method == 'POST':
        user.username = request.form['username']
        user.email = request.form['email']
        user.role_id = request.form['role_id']
        db.session.commit()
        flash('User updated successfully.', 'success')
        return redirect(url_for('admin.manage_users'))
    return render_template('admin/edit_user.html', user=user, roles=roles)

@admin_bp.route('/delete_user/<int:user_id>', methods=['POST'])
@login_required
@admin_required
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    if user.role.name == 'sysadmin':
        flash('Cannot delete admin users.', 'danger')
        return redirect(url_for('admin.manage_users'))
    db.session.delete(user)
    db.session.commit()
    flash('User deleted successfully.', 'success')
    return redirect(url_for('admin.manage_users'))

class CreateUserForm(FlaskForm):
    username = StringField('Username', [validators.DataRequired(), validators.Length(min=4, max=25)])
    email = StringField('Email', [validators.DataRequired(), validators.Email()])
    password = PasswordField('Password', [validators.DataRequired(), validators.Length(min=6)])
    first_name = StringField('First Name', [validators.DataRequired()])
    last_name = StringField('Last Name', [validators.DataRequired()])
    phone = StringField('Phone', [validators.DataRequired()])
    role_id = SelectField('Role', coerce=int, validators=[validators.DataRequired()])

@admin_bp.route('/create_user', methods=['GET', 'POST'])
@login_required
@admin_required
def create_user():
    form = CreateUserForm()
    
    # Get all roles and set them as choices for the role_id field
    roles = Role.query.all()
    form.role_id.choices = [(role.id, role.name) for role in roles]

    if form.validate_on_submit():
        try:
            # Check if username or email already exists
            if User.query.filter_by(username=form.username.data).first():
                flash('Username already exists.', 'danger')
                return render_template('admin/create_user.html', form=form)
            
            if User.query.filter_by(email=form.email.data).first():
                flash('Email already exists.', 'danger')
                return render_template('admin/create_user.html', form=form)

            # Create new user
            new_user = User(
                username=form.username.data,
                email=form.email.data,
                password_hash=generate_password_hash(form.password.data),
                first_name=form.first_name.data,
                last_name=form.last_name.data,
                phone=form.phone.data,
                role_id=form.role_id.data
            )

            db.session.add(new_user)
            db.session.commit()
            flash('User created successfully!', 'success')
            return redirect(url_for('admin.manage_users'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error creating user: {str(e)}', 'danger')
            return render_template('admin/create_user.html', form=form)

    # For GET requests or if form validation fails
    return render_template('admin/create_user.html', form=form) 