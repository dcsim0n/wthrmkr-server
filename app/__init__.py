# Import flask and template operators
from flask import Flask, render_template, jsonify

# Import SQLAlchemy
from flask_sqlalchemy import SQLAlchemy

# Define the WSGI application object
app = Flask(__name__)

# Configurations
app.config.from_object('config')

# Define the database object which is imported
db = SQLAlchemy(app)
# by modules and controllers


from app.models import Station, Location, Sensor, Measurment
@app.route('/stations')
def index():

    data = list( map(lambda s: s.name, Station.query.all()))
    return jsonify( data )

# Sample HTTP error handling
@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404


# Build the database:
# This will create the database file using SQLAlchemy
db.create_all()