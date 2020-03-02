from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema, auto_field
from flask_restful import Api, Resource
from database import Base
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship


class Pet(Base):
    __tablename__ = 'pet'
    id = Column(Integer, primary_key=True)
    first_name = Column(String(255))
    last_name = Column(String(255))
    age = Column(String(20))
    breed = Column(String(255))
    person_id = Column(Integer, ForeignKey('person.id'))

    def __init__(self, first_name=None, last_name=None, age=None, breed=None, person_id=None):
        self.first_name = first_name
        self.last_name = last_name
        self.age = age
        self.breed = breed
        self.person_id = person_id


class PetSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Pet
        include_fk = True


pet_schema = PetSchema()
pets_schema = PetSchema(many=True)


class PetListResource(Resource):
    def get(self):
        pets = Pet.query.all()
        return pets_schema.dump(pets)

    def post(self):
        new_post = Pet(
            first_name=request.json['first_name'],
            last_name=request.json['last_name'],
            age=request.json['age'],
            breed=request.json['breed'],
            person_id=request.json['person_id']
        )
        session.add(new_post)
        session.commit()
        return pet_schema.dump(new_post)


class PetResource(Resource):
    def get(self, pet_id):
        pet = Pet.query.get_or_404(pet_id)
        return pet_schema.dump(pet)

    def maybe_update(self, pet, field_name):
        if field_name in request.json:
            pet.first_name = request.json[field_name]

    def patch(self, pet_id):
        pet = Pet.query.get_or_404(pet_id)

        maybe_update(self, pet, "first_name")
        maybe_update(self, pet, "last_name")
        maybe_update(self, pet, "age")
        maybe_update(self, pet, "breed")
        maybe_update(self, pet, "person_id")

        session.commit()
        return pet_schema.dump(pet)

    def delete(self, pet_id):
        pet = Pet.query.get_or_404(pet_id)
        session.delete(pet)
        session.commit()
        return '', 204
