from flask_wtf import FlaskForm
from wtforms import TextField, PasswordField  # BooleanField

# Import Form validators
from wtforms.validators import Required, Email, EqualTo


# Define the login form (WTForms)

class AddressForm(FlaskForm):
    address = TextField('Address', [Required(message='Where do you live')])
    number = TextField('Street Number', [Required(
        message='Please add your Street Number')])
    street = TextField('Street Name', [Required(
        message='Must provide Street Name ;-)')])
    city = TextField('City', [Required(message='Please add your city.')])
    state = TextField('State', [Required(message='Please add your state')])
    zipcode = TextField('Zipcode', [Required(message='Your Zipcode please')])
