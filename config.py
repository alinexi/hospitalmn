import os
from datetime import timedelta

class Config:
    """Base configuration."""
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'your-secret-key-here'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') 
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Security settings
    DES_KEY_PATH = os.getenv('DES_KEY_PATH', 'instance/keys/des.key')
    RSA_PRIVATE_KEY_PATH = os.getenv('RSA_PRIVATE_KEY_PATH', 'instance/keys/private.pem')
    RSA_PUBLIC_KEY_PATH = os.getenv('RSA_PUBLIC_KEY_PATH', 'instance/keys/public.pem')
    
    # Session settings
    PERMANENT_SESSION_LIFETIME = timedelta(hours=1)
    SESSION_COOKIE_SECURE = True
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
    
    # CSRF protection
    WTF_CSRF_ENABLED = True
    WTF_CSRF_TIME_LIMIT = 3600  # 1 hour
    
    # File upload settings
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size
    UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'uploads')

class DevelopmentConfig(Config):
    """Development configuration."""
    DEBUG = True
    SQLALCHEMY_ECHO = True
    SESSION_COOKIE_SECURE = False

class TestingConfig(Config):
    """Testing configuration."""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'postgresql://localhost/hospital_test'
    WTF_CSRF_ENABLED = False

class ProductionConfig(Config):
    """Production configuration."""
    DEBUG = False
    TESTING = False
    
    # Production security settings
    SESSION_COOKIE_SECURE = True
    REMEMBER_COOKIE_SECURE = True
    SESSION_COOKIE_HTTPONLY = True
    REMEMBER_COOKIE_HTTPONLY = True

config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
} 