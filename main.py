from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_restful import Api, Resource




app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///dogwalker.db'
db = SQLAlchemy(app)
ma = Marshmallow(app)
from address import AddressListResource, AddressResource
from person import PersonListResource, PersonResource

api = Api(app)
db.init_app(app)
ma.init_app(app)
api.init_app(app)


api.add_resource(AddressListResource, '/addresses')
api.add_resource(AddressResource, '/addresses/<int:address_id>')
api.add_resource(PersonListResource, '/persons')
api.add_resource(PersonResource, '/persons/<int:person_id>')

if __name__ == '__main__':
  with app.test_request_context():
    db.create_all()
    db.session.commit()
  app.run(debug=True, host='0.0.0.0')

