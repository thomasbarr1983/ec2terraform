from flask_wtf import FlaskForm
from wtforms import TextField, PasswordField, HiddenField, FormField, FieldList
# Import Form validators
from wtforms.validators import Required, Email, EqualTo
from .pet import PetForm
from .address import AddressForm
# Define the login form (WTForms)

class PersonForm(FlaskForm):
    id = HiddenField('id')
    first_name = TextField(
        'First Name', [Required(message='Please add your First Name')])
    last_name = TextField('Last Name', [Required(
        message='Must provide Last Name ;-)')])
    phone_number = TextField(
        'first_name', [Required(message='Please add phone number.')])
    email = TextField('Email Address', [Email(),
                                        Required(message='Forgot your email address?')])


class PersonAndPetAndAddressForm(FlaskForm):
    id = HiddenField('id')
    first_name = TextField(
        'First Name', [Required(message='Please add your First Name')])
    last_name = TextField('Last Name', [Required(
        message='Must provide Last Name ;-)')])
    phone_number = TextField(
        'first_name', [Required(message='Please add phone number.')])
    email = TextField('Email Address', [Email(),
                                        Required(message='Forgot your email address?')])
    pets = FieldList(FormField(PetForm))
    address = FieldList(FormField(AddressForm))