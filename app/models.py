#!/usr/bin/env python

#-------------------------------------
# WTHR-MKR data modles
# Tim Walter and Dana simmons
#-------------------------------------

from app import db
from flask_sqlalchemy import SQLAlchemy

# class SensorType( db.Model):
#   id = db.Column( db.Integer , primary_key = True )
#   name = db.Column( db.String )
#   sensors = db.relationship('Sensor')

class Measurment(db.Model):
  id = db.Column( db.Integer, primary_key = True )
  name = db.Column( db.String )
  sensor_id = db.Column( db.Integer, db.ForeignKey('sensor.id'), nullable = False )
  sensor = db.relationship('Sensor', backref = db.backref('measurements', lazy = True ))

class Station(db.Model):
  id = db.Column( db.Integer , primary_key = True )
  name = db.Column( db.String )
  locations = db.relationship('Location')
  
class Location(db.Model):
  id = db.Column( db.Integer , primary_key = True )
  name = db.Column( db.String )
  sation_id = db.Column( db.Integer, db.ForeignKey('station.id'), nullable = False )
  
  station = db.relationship('Station')

class Sensor(db.Model):
  id = db.Column( db.Integer , primary_key = True )
  location_id = db.Column( db.Integer, db.ForeignKey('location.id'), nullable = False )
  # sensor_type_id = db.Column( db.Integer , db.ForeignKey('sensortype.id'), nullable = False )

  location = db.relationship('Location')
  # sensortype = db.relationship('SensorType')

 


