from flask import Blueprint, render_template, request, flash, redirect, url_for, abort
from flask_login import login_required, current_user
from app.models.user import User, Role
from app import db
from functools import wraps
import json
import os

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