from app import create_app, db
from app.models import User, Patient, Appointment

app = create_app()

with app.app_context():
    # Create all tables
    db.create_all()
    print("Tables created successfully!") 