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
    pets = relationship('Pet', backref='person')#cascade="all, delete-orphan"
    vet_id = Column(Integer, ForeignKey('person.id'))
    vet = relationship(lambda:Person, remote_side=id, backref="patients")

    def __init__(self, first_name=None, last_name=None, phone_number=None, email=None, role=None, vet_id=None):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.phone_number = phone_number
        self.vet_id = vet_id

    def __repr__(self):
        return '<Person %d,%s,%s,%s>' % self.id, self.first_name, self.last_name, self.role


