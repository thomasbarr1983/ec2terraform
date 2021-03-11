#Flask is our web application server framework, responsible for http framework and dispatching our code
from flask import Flask, request
#flask_sqlalchemy is a library that allows for object relational mapping as well as automated persistence of Python objects
from flask_sqlalchemy import SQLAlchemy
#flask_marshmallow thin integration layer for Flask and marshmallow (an object serialization/deserialization library) between json object and python object
from flask_marshmallow import Marshmallow
#allows for use of core services which we build the rest of our stuff
from marshmallow_sqlalchemy import SQLAlchemySchema, auto_field, SQLAlchemyAutoSchema
#flask_restful adds support for quickly building REST APIs
from flask_restful import Api, Resource
#DB Model for Address
from app.mod_dogwalker.models.address import Address
#DB ORM for Pet
from .pet import Pet
#Base is technically the SuperClass for all ORM handled by SQLAlchemy
from database import Base
#SQLAlchemy is the Python SQL toolkit and Object Relational Mapper
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship, sessionmaker

#set Person Model in DB on top of SQLAlchemy and create DB Table Person (primary key=the primary key of a relational table uniquely identifies each record in the table.)
class Person(Base):
    __tablename__ = 'person'
    id = Column(Integer, primary_key=True)
    first_name = Column(String(255))
    last_name = Column(String(255))
    phone_number = Column(String(255))
    email = Column(String(255))
    # will set up to have marker for dogwalker(w) or customer(c)
    role = Column(String(1))
    #sets relationship between address and person through primary key
    addresses = relationship('Address', backref='person')
    # cascade="all, delete-orphan"
    #sets relationship between pet and person through primary key
    pets = relationship('Pet', backref='person')
    #set vet id field in DB
    vet_id = Column(Integer, ForeignKey('person.id'))
    #set relationship between vet and patients/pet
    vet = relationship(lambda: Person, remote_side=id, backref="patients")

    def __init__(self, first_name=None, last_name=None, phone_number=None, email=None, role=None, vet_id=None):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.phone_number = phone_number
        self.vet_id = vet_id

    def __repr__(self):
        return '<Person %d,%s,%s,%s>' % self.id, self.first_name, self.last_name, self.role
