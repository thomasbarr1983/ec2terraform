from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from marshmallow_sqlalchemy import SQLAlchemySchema, auto_field
from flask_restful import Api, Resource
from sqlalchemy import Column, Integer, String, ForeignKey
from database import Base
from sqlalchemy.orm import relationship


class Address(Base):
    __tablename__ = 'address'
    id = Column(Integer, primary_key=True)
    number = Column(String(255))
    street = Column(String(255))
    city = Column(String(255))
    state = Column(String(255))
    zipcode = Column(String(255))
    person_id = Column(Integer, ForeignKey('person.id'))

    def __init__(self, number=None, street=None, city=None, state=None, zipcode=None, person_id=None):
        self.number = number
        self.street = street
        self.city = city
        self.state = state
        self.zipcode = zipcode
        self.person_id = person_id

    def __repr__(self):
        return '<Address %d,%s,%s>' % self.id, self.number, self.street




