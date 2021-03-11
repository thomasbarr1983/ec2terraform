#Flask is our web application server framework, responsible for http framework and dispatching our code
from flask import Flask, request
#flask_sqlalchemy is a library that allows for object relational mapping as well as automated persistence of Python objects
from flask_sqlalchemy import SQLAlchemy
#flask_marshmallow thin integration layer for Flask and marshmallow (an object serialization/deserialization library) between json object and python object
from flask_marshmallow import Marshmallow
#allows for use of core services which we build the rest of our stuff
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema, auto_field
#flask_restful adds support for quickly building REST APIs
from flask_restful import Api, Resource
from database import Base
#SQLAlchemy is the Python SQL toolkit and Object Relational Mapper
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

#set Pet Model in DB on top of SQLAlchemy and create DB Table Pet (primary key=the primary key of a relational table uniquely identifies each record in the table.)
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
