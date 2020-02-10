from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_restful import Api, Resource
from app import app, db, ma
from address import AddressListResource, AddressResource
from person import PersonListResource, PersonResource, PersonSearchResource
from pet import PetListResource, PetResource

api = Api(app)


api.add_resource(AddressListResource, '/addresses')
api.add_resource(AddressResource, '/addresses/<int:address_id>')
api.add_resource(PersonListResource, '/persons')
api.add_resource(PersonResource, '/persons/<int:person_id>')
api.add_resource(PersonSearchResource, '/persons/search/<search_term>')
api.add_resource(PetListResource, '/pets')
api.add_resource(PetResource, '/pets/<int:pet_id>')


if __name__ == '__main__':
    with app.test_request_context():
        db.create_all()
        db.session.commit()
    app.run(debug=True, host='0.0.0.0')
