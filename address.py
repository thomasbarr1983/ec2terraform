from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_restful import Api, Resource

db = SQLAlchemy()
ma = Marshmallow()


class Address(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    number = db.Column(db.String(255))
    street = db.Column(db.String(255))
    city = db.Column(db.String(255))
    state = db.Column(db.String(255))
    zipcode = db.Column(db.String(255))
    person_id = db.Column(db.Integer,db.ForeignKey('person.id'))

    def __repr__(self):
        return '<Address %d,%s,%s>' % self.id,self.number,self.street

class AddressSchema(ma.Schema):
        class Meta:
                fields = ("id", "number", "street", "city", "state", "zipcode")

address_schema = AddressSchema()
addresses_schema = AddressSchema(many=True)


class AddressListResource(Resource):
    def get(self):
        addresses = Address.query.all()
        return addresses_schema.dump(addresses)

    def post(self):
        new_post = Address(
                number=request.json['number'],
                street=request.json['street'],
                city=request.json['city'],
                state=request.json['state'],
                zipcode=request.json['zipcode']
        )
        db.session.add(new_post)
        db.session.commit()
        return address_schema.dump(new_post)





class AddressResource(Resource):
    def get(self, address_id):
        address = Address.query.get_or_404(address_id)
        return address_schema.dump(address)

    def patch(self, address_id):
        address = Address.query.get_or_404(address_id)

        if 'number' in request.json:
           address.number = request.json['number']
        if 'street' in request.json:
           address.street = request.json['street']
        if 'city' in request.json:
           address.city = request.json['city']
        if 'state' in request.json:
           address.state = request.json['state']      
        if 'zipcode' in request.json:
           address.zipcode = request.json['zipcode']
              
        db.session.commit()
        return address_schema.dump(address)


    def delete(self, address_id):
        address = Address.query.get_or_404(address_id)
        db.session.delete(address)
        db.session.commit()
        return '', 204




