from flask import request, render_template, \
    flash, g, session, redirect, url_for
from database import db_session
# Import the database object from the main app module
from flask_smorest import Api, Blueprint, abort
from app import db
from .models.pet import Pet
from .models.person import Person
from .models.address import Address
# Import module forms
from .forms.person import PersonForm
from .forms.pet import PetForm
from .forms.address import AddressForm
# Import module models (i.e. User)


# Define the blueprint: 'auth', set its url prefix: app.url/auth
mod_dogwalker = Blueprint('dogwalker', __name__, url_prefix='/dogwalker')

# Set the route and accepted methods


@mod_dogwalker.route('/person', methods=['GET', 'POST'])
def create_person():

    # If sign in form is submitted
    form = PersonForm(request.form)

    # Verify the sign in form
    if form.validate_on_submit():

        new_person = Person(first_name=form.first_name.data, last_name=form.last_name.data,
                            phone_number=form.phone_number.data, email=form.email.data, role='C')
        db_session.add(new_person)
        db_session.commit()

    return render_template("person.html", form=form)


@mod_dogwalker.route('/persons/<person_id>', methods=['GET', 'POST'])
def view_person(person_id):

    person = Person.query.get(person_id)
    form = PersonForm()
    form.process(formdata=request.form, obj=person)
    if request.method == 'POST' and form.validate():
        form.populate_obj(person)
        session.commit()
        redirect('/persons/'+person_id)
    return render_template('person.html', form=form)


@mod_dogwalker.route('/pet', methods=['GET', 'POST'])
def create_pet():

    form = PetForm(request.form)

    # Verify the sign in form
    if form.validate_on_submit():

        new_pet = Pet(first_name=form.first_name.data,
                      last_name=form.last_name.data, breed=form.breed.data, age=form.age.data)
        db_session.add(new_pet)
        db_session.commit()

    return render_template("pet.html", form=form)


@mod_dogwalker.route('/address', methods=['GET', 'POST'])
def create_address():

    form = AddressForm(request.form)

    # Verify the sign in form
    if form.validate_on_submit():

        new_address = Address(number=form.number.data, street=form.street.data,
                              city=form.city.data, state=form.state.data, zipcode=form.zipcode.data)
        db_session.add(new_address)
        db_session.commit()

    return render_template("address.html", form=form)
