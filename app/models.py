#!/usr/bin/env python

#-------------------------------------
# WTHR-MKR data modles
# Tim Walter and Dana simmons
#-------------------------------------

from app import db
from flask_sqlalchemy import SQLAlchemy
import requests

class SensorType( db.Model):
  id = db.Column( db.Integer , primary_key = True )
  name = db.Column( db.String )
  measurments = db.relationship('Measurment')

class Measurment(db.Model):
  id = db.Column( db.Integer, primary_key = True )
  name = db.Column( db.String )
  location_id = db.Column( db.Integer, db.ForeignKey('location.id'), nullable = False )
  sensor_type_id = db.Column( db.Integer, db.ForeignKey('sensor_type.id'), nullable = False )

  sensor_type = db.relationship( 'SensorType' )
  location = db.relationship( 'Location' )

class Station(db.Model):
  id = db.Column( db.Integer , primary_key = True )
  name = db.Column( db.String )
  address = db.Column( db.String )
  locations = db.relationship('Location')
  measurements = db.relationship('Measurment', secondary='location' )

  def read_all(self):
    req = requests.get(self.address)
    data = req.json() # Convert data to json
    assert 'locations' in data, "Data is not a valid response from station"
    print(data) # print info for debugging
    for location, sensors in data.locations:
      self.locations.append(location)
      self.sensors.append(sensors)
    

  
class Location(db.Model):
  id = db.Column( db.Integer , primary_key = True )
  name = db.Column( db.String )
  sation_id = db.Column( db.Integer, db.ForeignKey('station.id'), nullable = False )

  measurments = db.relationship('Measurment')
  station = db.relationship('Station')
