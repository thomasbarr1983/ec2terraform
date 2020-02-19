# Import flask dependencies
from flask import Blueprint, request, render_template, \
    flash, g, session, redirect, url_for
from database import db_session
# Import the database object from the main app module
from app import db

# Import module forms
from .forms.person import PersonForm

# Import module models (i.e. User)
from .models.person import Person

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

