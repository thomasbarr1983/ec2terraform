from flask_wtf import FlaskForm
from wtforms import TextField, PasswordField  # BooleanField

# Import Form validators
from wtforms.validators import Required, Email, EqualTo


# Define the login form (WTForms)

class PersonForm(FlaskForm):
    first_name = TextField(
        'First Name', [Required(message='Please add your First Name')])
    last_name = TextField('Last Name', [Required(
        message='Must provide Last Name ;-)')])
    phone_number = TextField(
        'first_name', [Required(message='Please add phone number.')])
    email = TextField('Email Address', [Email(),
                                        Required(message='Forgot your email address?')])
