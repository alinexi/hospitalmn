import pytest
from app import create_app, db
from app.models.user import User, Role
from flask_login import current_user

@pytest.fixture
def app():
    app = create_app('testing')
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def runner(app):
    return app.test_cli_runner()

def test_login_page(client):
    response = client.get('/login')
    assert response.status_code == 200
    assert b'Log In' in response.data

def test_register_page(client):
    response = client.get('/register')
    assert response.status_code == 200
    assert b'Register' in response.data

def test_registration(client):
    response = client.post('/register', data={
        'username': 'testuser',
        'email': 'test@example.com',
        'first_name': 'Test',
        'last_name': 'User',
        'phone': '1234567890',
        'password': 'testpass123',
        'password2': 'testpass123'
    }, follow_redirects=True)
    assert response.status_code == 200
    assert b'Registration successful' in response.data

def test_login_logout(client):
    # Create a test user
    with client.application.app_context():
        role = Role(name='patient', description='Patient')
        db.session.add(role)
        user = User(
            username='testuser',
            email='test@example.com',
            first_name='Test',
            last_name='User',
            role=role
        )
        user.password = 'testpass123'
        db.session.add(user)
        db.session.commit()

    # Test login
    response = client.post('/login', data={
        'username': 'testuser',
        'password': 'testpass123',
        'remember_me': False
    }, follow_redirects=True)
    assert response.status_code == 200
    assert b'Welcome' in response.data

    # Test logout
    response = client.get('/logout', follow_redirects=True)
    assert response.status_code == 200
    assert b'You have been logged out' in response.data

def test_invalid_login(client):
    response = client.post('/login', data={
        'username': 'nonexistent',
        'password': 'wrongpass',
        'remember_me': False
    }, follow_redirects=True)
    assert response.status_code == 200
    assert b'Invalid username or password' in response.data

def test_duplicate_registration(client):
    # Create initial user
    with client.application.app_context():
        role = Role(name='patient', description='Patient')
        db.session.add(role)
        user = User(
            username='testuser',
            email='test@example.com',
            first_name='Test',
            last_name='User',
            role=role
        )
        user.password = 'testpass123'
        db.session.add(user)
        db.session.commit()

    # Try to register with same username
    response = client.post('/register', data={
        'username': 'testuser',
        'email': 'another@example.com',
        'first_name': 'Another',
        'last_name': 'User',
        'phone': '1234567890',
        'password': 'testpass123',
        'password2': 'testpass123'
    }, follow_redirects=True)
    assert response.status_code == 200
    assert b'Please use a different username' in response.data 