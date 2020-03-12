from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from app import app, db, ma, api
#from app.mod_dogwalker.rest.address import AddressListResource, AddressResource
#from app.mod_dogwalker.rest.person import PersonListResource, PersonResource, PersonSearchResource
#from app.mod_dogwalker.rest.pet import PetListResource, PetResource
from app.mod_auth.models import User, Role
from database import db_session
from flask_security import Security, SQLAlchemySessionUserDatastore, login_required, current_user
from database import init_db
from app.mod_dogwalker.controllers import mod_dogwalker
from flask_smorest import Api, Blueprint, abort
from app.mod_dogwalker.rest.pet import blp as pet_blp
from app.mod_dogwalker.rest.person import blp as person_blp
from app.mod_dogwalker.rest.address import blp as address_blp


init_db()


@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()


# Register form blueprints
app.register_blueprint(mod_dogwalker)
# Register rest api bluprints
api.register_blueprint(pet_blp)
api.register_blueprint(person_blp)
api.register_blueprint(address_blp)

user_datastore = SQLAlchemySessionUserDatastore(db_session, User, Role)
security = Security(app, user_datastore)

# Create a user to test with


@app.before_first_request
def create_user():

    # user_datastore.create_user(email='thomas.barr1983@gmail.com', password='Bassai1983!#%&')
    db_session.commit()

# Views


@app.route('/')
@login_required
def home():
    return ('Here you go! '+current_user.email)


if __name__ == '__main__':
    with app.test_request_context():
        db.create_all()
        db.session.commit()
    app.run(debug=True, host='0.0.0.0')
