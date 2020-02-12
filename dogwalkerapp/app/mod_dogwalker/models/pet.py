from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema, auto_field
from flask_restful import Api, Resource
from app import db, ma


class Pet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(255))
    last_name = db.Column(db.String(255))
    age = db.Column(db.String(20))
    breed = db.Column(db.String(255))
    person_id = db.Column(db.Integer, db.ForeignKey('person.id'))


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
        db.session.add(new_post)
        db.session.commit()
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

        db.session.commit()
        return pet_schema.dump(pet)

    def delete(self, pet_id):
        pet = Pet.query.get_or_404(pet_id)
        db.session.delete(pet)
        db.session.commit()
        return '', 204
