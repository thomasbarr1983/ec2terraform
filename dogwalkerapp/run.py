from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_restful import Api, Resource
from app import app, db, ma
from app.mod_dogwalker.models.address import AddressListResource, AddressResource
from app.mod_dogwalker.models.person import PersonListResource, PersonResource, PersonSearchResource
from app.mod_dogwalker.models.pet import PetListResource, PetResource
from app.mod_auth.models import User, Role
from database import db_session
from flask_security import Security, SQLAlchemySessionUserDatastore, login_required, current_user
from database import init_db
api = Api(app)
init_db()
@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()

api.add_resource(AddressListResource, '/addresses')
api.add_resource(AddressResource, '/addresses/<int:address_id>')
api.add_resource(PersonListResource, '/persons')
api.add_resource(PersonResource, '/persons/<int:person_id>')
api.add_resource(PersonSearchResource, '/persons/search/<search_term>')
api.add_resource(PetListResource, '/pets')
api.add_resource(PetResource, '/pets/<int:pet_id>')


user_datastore = SQLAlchemySessionUserDatastore(db_session, User, Role)
security = Security(app, user_datastore)

# Create a user to test with
@app.before_first_request
def create_user():
    
    #user_datastore.create_user(email='thomas.barr1983@gmail.com', password='Bassai1983!#%&')
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



