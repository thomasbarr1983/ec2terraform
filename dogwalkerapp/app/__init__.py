from app.mod_auth.controllers import mod_auth as auth_module
from flask import Flask, render_template
from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy
from flask_smorest import Api

# Define the WSGI application object
app = Flask(__name__)

# Configurations
app.config.from_object('config')
api = Api(app)
# Define the database object which is imported
# by modules and controllers
db = SQLAlchemy(app)
ma = Marshmallow(app)
# Sample HTTP error handling


@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404


# Import a module / component using its blueprint handler variable (mod_auth)

# Register blueprint(s)
app.register_blueprint(auth_module)
# app.register_blueprint(xyz_module)
# ..

# Build the database:
# This will create the database file using SQLAlchemy

db.create_all()
