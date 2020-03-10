from flask import Flask
from flask_security import Security, login_required, \
    SQLAlchemySessionUserDatastore
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow


#app = Flask(__name__)
# app.config["SQLALCHEMY_DATABASE_URI"]="sqlite:///dogwalker.db"
#db = SQLAlchemy(app)
#ma = Marshmallow(app)
