from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from app.models.user import User

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[
        DataRequired(),
        Length(min=3, max=64)
    ])
    password = PasswordField('Password', validators=[
        DataRequired(),
        Length(min=6)
    ])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Log In')

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[
        DataRequired(),
        Length(min=3, max=64)
    ])
    email = StringField('Email', validators=[
        DataRequired(),
        Email(),
        Length(max=120)
    ])
    first_name = StringField('First Name', validators=[
        DataRequired(),
        Length(max=64)
    ])
    last_name = StringField('Last Name', validators=[
        DataRequired(),
        Length(max=64)
    ])
    phone = StringField('Phone Number', validators=[
        DataRequired(),
        Length(max=20)
    ])
    role = SelectField('Role', choices=[
        ('sysadmin', 'System Administrator'),
        ('receptionist', 'Receptionist'),
        ('chief_doctor', 'Chief Doctor'),
        ('curing_doctor', 'Curing Doctor'),
        ('consulting_doctor', 'Consulting Doctor'),
        ('patient', 'Patient')
    ], validators=[DataRequired()])
    password = PasswordField('Password', validators=[
        DataRequired(),
        Length(min=6)
    ])
    password2 = PasswordField('Confirm Password', validators=[
        DataRequired(),
        EqualTo('password', message='Passwords must match.')
    ])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.') 