from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import marshmallow as ma
from marshmallow_sqlalchemy import SQLAlchemySchema, auto_field, SQLAlchemyAutoSchema
from flask_restful import Api, Resource
from app.mod_dogwalker.models.address import Address
from .pet import Pet
from database import Base
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship, sessionmaker
from ..models.person import Person
from flask.views import MethodView
from flask_smorest import Api, Blueprint, abort
from ... import api

blp = Blueprint(
    'persons', 'persons', url_prefix='/persons',
    description='Operations on persons'
)


class PersonSchema(SQLAlchemySchema):
    class Meta:
        model = Person
        include_fk = True

    id = auto_field()
    first_name = auto_field()
    last_name = auto_field()
    phone_number = auto_field()
    email = auto_field()
    role = auto_field()
    addresses = auto_field()
    pets = auto_field()
    vet = auto_field()


class PersonQueryArgsSchema(ma.Schema):
    name = ma.fields.String()


class PersonFullSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Person
        include_relationships = True
        load_instance = True


@blp.route('/')
class PersonListResource(MethodView):
    @blp.arguments(PersonQueryArgsSchema, location='query')
    @blp.response(PersonSchema(many=True))
    def get(self, args):
        """List persons

        Get list of persons"""
        return persons.query.all()

    @blp.arguments(PersonSchema)
    @blp.response(PersonSchema, code=201)
    def post(self, new_data):
        """Add a new person"""
        new_post = Person(
            first_name=request.json['first_name'],
            last_name=request.json['last_name'],
            phone_number=request.json['phone_number'],
            email=request.json['email'],
            role=request.json['role'],
            vet=request.json['vet']
        )
        session.add(new_post)
        session.commit()
        return new_post


@blp.route('/<person_id>')
class PersonResource(MethodView):
    @blp.response(PersonSchema)
    def get(self, person_id):
        """Get person by ID"""

        person = Person.query.get(person_id)
        if person is None:
            abort(404, message='Item not found.')
        return person

    @blp.arguments(PersonSchema)
    @blp.response(PersonSchema)
    def patch(self, new_data, person_id):
        """Update existing person"""

        person = Person.query.get(person_id)
        if person is None:
            abort(404, message='Item not found.')

        if 'first_name' in request.json:
            person.number = request.json['first_name']
        if 'last_name' in request.json:
            person.street = request.json['last_name']
        if 'phone_number' in request.json:
            person.city = request.json['phone_number']
        if 'email' in request.json:
            person.state = request.json['email']
        if 'role' in request.json:
            person.zipcode = request.json['role']
        if 'vet' in request.json:
            person.vet = request.json['vet']

        session.commit()
        return person

    @blp.response(code=204)
    def delete(self, person_id):
        """Delete pet"""
        person = Person.query.get(person_id)
        if person is None:
            abort(404, message='Item not found.')
        session.delete(person)
        session.commit()


class PersonSearchArgsSchema(ma.Schema):
    name = ma.fields.String()


class PersonSearchResource(MethodView):
    @blp.arguments(PersonSearchArgsSchema, location='query')
    @blp.response(PersonSchema(many=True))
    def get(self,  args):
        results = Person.query.filter(
            Person.first_name.like('%'+args+'%')).all()
        return results
