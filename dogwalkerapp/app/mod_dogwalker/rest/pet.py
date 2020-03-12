from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import marshmallow as ma
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema, auto_field
from flask_restful import Api, Resource
from database import Base
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from ..models.pet import Pet
from flask.views import MethodView
from flask_smorest import Api, Blueprint, abort
from ... import api

blp = Blueprint(
    'pets', 'pets', url_prefix='/pets',
    description='Operations on pets'
)


class PetSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Pet
        include_fk = True
        load_instance = True


class PetQueryArgsSchema(ma.Schema):
    name = ma.fields.String()


@blp.route('/')
class PetListResource(MethodView):
    @blp.arguments(PetQueryArgsSchema, location='query')
    @blp.response(PetSchema(many=True))
    def get(self, args):
        """List pets

        Get list of pets"""
        return Pet.query.all()

    @blp.arguments(PetSchema)
    @blp.response(PetSchema, code=201)
    def post(self, new_data):
        """Add a new pet"""
        new_post = Pet(
            first_name=new_data['first_name'],
            last_name=new_data['last_name'],
            age=new_data['age'],
            breed=new_data['breed'],
            person_id=new_data['person_id']
        )
        session.add(new_post)
        session.commit()
        return new_post


@blp.route('/<pet_id>')
class PetResource(MethodView):
    @blp.response(PetSchema)
    def get(self, pet_id):
        """Get pet by ID"""

        pet = Pet.query.get(pet_id)
        if pet is None:
            abort(404, message='Item not found.')
        return pet

    def maybe_update(self, pet, field_name):
        if field_name in new_data.json:
            pet.first_name = new_data.json[field_name]

    @blp.arguments(PetSchema)
    @blp.response(PetSchema)
    def patch(self, new_data, pet_id):
        """Update existing pet"""

        pet = Pet.query.get(pet_id)
        if pet is None:
            abort(404, message='Item not found.')

        maybe_update(self, pet, "first_name")
        maybe_update(self, pet, "last_name")
        maybe_update(self, pet, "age")
        maybe_update(self, pet, "breed")
        maybe_update(self, pet, "person_id")

        session.commit()
        return pet

    @blp.response(code=204)
    def delete(self, pet_id):
        """Delete pet"""
        pet = Pet.query.get(pet_id)
        if pet is None:
            abort(404, message='Item not found.')
        session.delete(pet)
        session.commit()
