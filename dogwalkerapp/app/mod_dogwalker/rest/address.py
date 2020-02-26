from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import marshmallow as ma
from marshmallow_sqlalchemy import SQLAlchemySchema, auto_field
from flask_restful import Api, Resource
from sqlalchemy import Column, Integer, String, ForeignKey
from database import Base
from sqlalchemy.orm import relationship
from ..models.address import Address
from flask.views import MethodView
from flask_smorest import Api, Blueprint, abort
from ... import api

blp = Blueprint(
    'address', 'address', url_prefix='/addresses',
    description='Operations on address'
)
class AddressSchema(SQLAlchemySchema):
    class Meta:
        model = Address
        include_fk = True
    id = auto_field()
    number = auto_field()
    street = auto_field()
    city = auto_field()
    state = auto_field()
    zipcode = auto_field()
    person_id = auto_field()


address_schema = AddressSchema()
addresses_schema = AddressSchema(many=True)

class AddressQueryArgsSchema(ma.Schema):
    name = ma.fields.String()


@blp.route('/')
class AddressListResource(MethodView):
    @blp.arguments(AddressQueryArgsSchema, location='query')
    @blp.response(AddressSchema(many=True))
    def get(self, args):
        """List address

        Get list of addresses"""
        return Address.query.all()
    @blp.arguments(AddressSchema)
    @blp.response(AddressSchema, code=201)
    def post(self, new_data):
        new_post = Address(
            number=request.json['number'],
            street=request.json['street'],
            city=request.json['city'],
            state=request.json['state'],
            zipcode=request.json['zipcode'],
            person_id=request.json['person_id']
        )
        session.add(new_post)
        session.commit()
        return new_post

@blp.route('/<address_id>')
class AddressResource(MethodView):
    @blp.response(AddressSchema)
    def get(self, address_id):
        """Get address by ID"""

        address = Address.query.get(address_id)
        if address is None:
            abort(404, message='Item not found.')
        return address

    @blp.arguments(AddressSchema)
    @blp.response(AddressSchema)
    def patch(self, new_data, address_id):
        """Update existing address"""
        address = Address.query.get(address_id)
        if address is None:
            abort(404, message='Item not found.')

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
        if 'person_id' in request.json:
            address.person_id = request.json['person_id']

        session.commit()
        return address_schema.dump(address)

    @blp.response(code=204)
    def delete(self, address_id):
        """Delete pet"""
        address = Address.query.get(address_id)
        if address is None:
            abort(404, message='Item not found')
        session.delete(address)
        session.commit()
        return '', 204
