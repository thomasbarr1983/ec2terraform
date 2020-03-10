from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from marshmallow_sqlalchemy import SQLAlchemySchema, auto_field, SQLAlchemyAutoSchema
from flask_restful import Api, Resource
from app.mod_dogwalker.models.address import Address
from .pet import Pet
from database import Base
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship, sessionmaker


class Person(Base):
    __tablename__ = 'person'
    id = Column(Integer, primary_key=True)
    first_name = Column(String(255))
    last_name = Column(String(255))
    phone_number = Column(String(255))
    email = Column(String(255))
    # will set up to have marker for dogwalker(w) or customer(c)
    role = Column(String(1))
    addresses = relationship('Address', backref='person')
    # cascade="all, delete-orphan"
    pets = relationship('Pet', backref='person')
    vet_id = Column(Integer, ForeignKey('person.id'))
    vet = relationship(lambda: Person, remote_side=id, backref="patients")

    def __init__(self, first_name=None, last_name=None, phone_number=None, email=None, role=None, vet_id=None):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.phone_number = phone_number
        self.vet_id = vet_id

    def __repr__(self):
        return '<Person %d,%s,%s,%s>' % self.id, self.first_name, self.last_name, self.role


class PersonSchema(SQLAlchemySchema):
    class Meta:
        model = Person
    id = auto_field()
    first_name = auto_field()
    last_name = auto_field()
    phone_number = auto_field()
    email = auto_field()
    role = auto_field()
    addresses = auto_field()
    pets = auto_field()
    vet = auto_field()


person_schema = PersonSchema()
persons_schema = PersonSchema(many=True)


class PersonFullSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Person
        include_relationships = True
        load_instance = True


person_full_schema = PersonFullSchema()
persons_full_schema = PersonFullSchema(many=True)


class PersonListResource(Resource):
    def get(self):
        persons = Person.query.all()
        return persons_full_schema.dump(persons)

    def post(self):
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
        return person_schema.dump(new_post)


class PersonResource(Resource):
    def get(self, person_id):
        person = Person.query.get_or_404(person_id)
        return person_schema.dump(person)

    def patch(self, person_id):
        person = Person.query.get_or_404(person_id)

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
        return person_schema.dump(person)

    def delete(self, person_id):
        person = Person.query.get_or_404(person_id)
        session.delete(person)
        session.commit()
        return '', 204


class PersonSearchResource(Resource):
    def get(self, search_term):
        results = Person.query.filter(
            Person.first_name.like('%'+search_term+'%')).all()
        return persons_schema.dump(results)
