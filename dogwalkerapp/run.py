#Flask is our web application server framework, responsible for http framework and dispatching our code
from flask import Flask, request
#flask_sqlalchemy is a library that allows for object relational mapping as well as automated persistence of Python objects
from flask_sqlalchemy import SQLAlchemy
#flask_marshmallow thin integration layer for Flask and marshmallow (an object serialization/deserialization library) between json object and python object
from flask_marshmallow import Marshmallow
#allows for use of core services which we build the rest of our stuff
from app import app, db, ma, api
#login support (defines DB models for login objects)
from app.mod_auth.models import User, Role
#provides connection to DB
from database import db_session
#flask_security allows for quick add common security mechanisms to your Flask application
from flask_security import Security, SQLAlchemySessionUserDatastore, login_required, current_user
#from database initialize the database (throw the switch Igor)
from database import init_db
#from app/model_dogwalker controllers import model dogwalker
from app.mod_dogwalker.controllers import mod_dogwalker
#flask_smorest database-agnostic framework library for creating REST APIs.
from flask_smorest import Api, Blueprint, abort
#provides restAPI controller purpose being to route traffic from URL to appropriate place
from app.mod_dogwalker.rest.pet import blp as pet_blp
from app.mod_dogwalker.rest.person import blp as person_blp
from app.mod_dogwalker.rest.address import blp as address_blp

#initialize DB
init_db()

#allows for clean shutdown, and flushes DB and then closes it
@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()


# Register form blueprints
app.register_blueprint(mod_dogwalker)
# Register rest api bluprints
api.register_blueprint(pet_blp)
api.register_blueprint(person_blp)
api.register_blueprint(address_blp)
#creating object of SQLAlchemySessionUserDatastore to set up user security while logged in using the db_session (it's a wrapper)
user_datastore = SQLAlchemySessionUserDatastore(db_session, User, Role)
security = Security(app, user_datastore)



# Create a user to test with
@app.before_first_request
def create_user():

    # user_datastore.create_user(email='thomas.barr1983@gmail.com', password='Bassai1983!#%&') forces data to be written to DB from memory
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
    #0.0.0.0 = listen to all host connecting IP addresses
