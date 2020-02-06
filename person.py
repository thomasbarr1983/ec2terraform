from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_restful import Api, Resource
from address import Address

db = SQLAlchemy()
ma = Marshmallow()


class Person(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(255))
    last_name = db.Column(db.String(255))
    phone_number = db.Column(db.String(255))
    email = db.Column(db.String(255))
    role = db.Column(db.String(1)) #will set up to have marker for dogwalker(w) or customer(c)
    addresses = db.relationship('Address',backref='person')

    def __repr__(self):
        return '<Person %d,%s,%s,%s>' % self.id,self.first_name,self.last_name, self.role

class PersonSchema(ma.Schema):
        class Meta:
                fields = ("id", "first_name", "last_name", "phone_number", "email", "role")

person_schema = PersonSchema()
persons_schema = PersonSchema(many=True)


class PersonListResource(Resource):
    def get(self):
        persons = Person.query.all()
        return persons_schema.dump(persons)

    def post(self):
        new_post = Person(
                first_name=request.json['first_name'],
                last_name=request.json['last_name'],
                phone_number=request.json['phone_number'],
                email=request.json['email'],
                role=request.json['role']
        )
        db.session.add(new_post)
        db.session.commit()
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
              
        db.session.commit()
        return person_schema.dump(person)


    def delete(self, person_id):
        person = Person.query.get_or_404(person_id)
        db.session.delete(person)
        db.session.commit()
        return '', 204




