from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_wtf.csrf import CSRFProtect
from config import config

# Initialize extensions
db = SQLAlchemy()
login_manager = LoginManager()
migrate = Migrate()
csrf = CSRFProtect()

def create_app(config_name='default'):
    """Application factory function."""
    app = Flask(__name__)
    app.config.from_object(config[config_name])

    # Initialize extensions with app
    db.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app, db)
    csrf.init_app(app)

    # Configure login
    login_manager.login_view = 'auth.login'
    login_manager.login_message = 'Please log in to access this page.'
    login_manager.login_message_category = 'info'

    # Register blueprints
    from app.views.auth import auth_bp
    from app.views.admin import admin_bp
    from app.views.patient import patient_bp
    from app.views.receptionist import receptionist_bp
    from app.views.main import main_bp
    from app.views.chief_doctor import chief_doctor_bp
    from app.views.curing_doctor import curing_doctor_bp
    from app.views.consulting_doctor import consulting_doctor_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(patient_bp)
    app.register_blueprint(receptionist_bp)
    app.register_blueprint(main_bp)
    app.register_blueprint(chief_doctor_bp)
    app.register_blueprint(curing_doctor_bp)
    app.register_blueprint(consulting_doctor_bp)

    # Register error handlers
    from app.utils.error_handlers import register_error_handlers
    register_error_handlers(app)

    # Register CLI commands
    from app.cli import init_app as init_cli
    init_cli(app)

    return app 