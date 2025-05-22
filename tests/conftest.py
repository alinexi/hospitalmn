import pytest
from app import create_app, db
from app.models.user import User, Role

@pytest.fixture(scope='session')
def app():
    """Create application for the tests."""
    app = create_app('testing')
    return app

@pytest.fixture(scope='session')
def _db(app):
    """Create database for the tests."""
    with app.app_context():
        db.create_all()
        yield db
        db.session.remove()
        db.drop_all()

@pytest.fixture(scope='function')
def session(_db):
    """Create a new database session for a test."""
    connection = _db.engine.connect()
    transaction = connection.begin()
    
    options = dict(bind=connection, binds={})
    session = _db.create_scoped_session(options=options)
    
    _db.session = session
    
    yield session
    
    transaction.rollback()
    connection.close()
    session.remove()

@pytest.fixture
def client(app):
    """Create a test client."""
    return app.test_client()

@pytest.fixture
def runner(app):
    """Create a test CLI runner."""
    return app.test_cli_runner()

@pytest.fixture
def admin_user(session):
    """Create an admin user for testing."""
    role = Role(name='sysadmin', description='System Administrator')
    session.add(role)
    session.commit()
    
    user = User(
        username='admin',
        email='admin@example.com',
        first_name='Admin',
        last_name='User',
        role=role
    )
    user.password = 'admin123'
    session.add(user)
    session.commit()
    return user

@pytest.fixture
def patient_user(session):
    """Create a patient user for testing."""
    role = Role(name='patient', description='Patient')
    session.add(role)
    session.commit()
    
    user = User(
        username='patient',
        email='patient@example.com',
        first_name='Test',
        last_name='Patient',
        role=role
    )
    user.password = 'patient123'
    session.add(user)
    session.commit()
    return user 