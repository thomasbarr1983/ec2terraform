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
