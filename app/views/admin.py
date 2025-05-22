from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask import Blueprint, render_template
from flask_login import login_required, current_user
from functools import wraps
from flask import abort
from flask_sqlalchemy import SQLAlchemy

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
    # Logic to manage system settings
    return render_template('admin/settings.html')

@admin_bp.route('/audit_logs', methods=['GET'])
@login_required
@admin_required
def view_audit_logs():
    # Logic to view audit logs
    return render_template('admin/audit_logs.html') 