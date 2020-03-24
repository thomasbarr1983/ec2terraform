from flask_wtf import FlaskForm
from wtforms import TextField, PasswordField, HiddenField

# Import Form validators
from wtforms.validators import Required, Email, EqualTo


# Define the login form (WTForms)

class PetForm(FlaskForm):
    person_id = HiddenField('person_id')
    first_name = TextField('First Name', [Required(message='Please add your pets First Name')])
    last_name = TextField('Last Name', [Required(message='Must provide Last Name ;-)')])
    age = TextField('Pets Age', [Required(message='What is your pets age?')])
    breed = TextField('Breed', [Required(message='What is your pets breed?')])
