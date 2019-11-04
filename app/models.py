#!/usr/bin/env python

#-------------------------------------
# WTHR-MKR data modles
# Tim Walter and Dana simmons
#-------------------------------------

from app.app import db

class Measurment(db.Model):
  id = db.Column( db.Integer, primary_key = True )
  name = db.Column( db.String )
  sensor_id = db.Column( db.Integer )
  #Stuf stuf stuf


class Station(db.Model):
  #Stuf stuf stuf
  id = db.Column( db.Integer , primary_key = True )
  name = db.Column( db.String )
  
class Location(db.Model):
  id = db.Column( db.Integer , primary_key = True )
  sation_id = db.Column( db.Integer )
  name = db.Column( db.String )
  #SStuf stuf stuf

class Sensor(db.Model):
  id = db.Column( db.integer , primary_key = True )
  location_id = db.Column( db.Intger )
  sensor_type_id = db.Column( db.Integer )

class SensorType( db.Model):
  id = db.Column( db.integer , primary_key = True )
  name = db.Column( db.String )
 #All the stufy stuf


