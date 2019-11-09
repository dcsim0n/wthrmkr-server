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
  value = db.Column( db.Decimal )
  location_id = db.Column( db.Integer, db.ForeignKey('location.id'), nullable = False )
  sensor_type_id = db.Column( db.Integer, db.ForeignKey('sensor_type.id'), nullable = False )

  sensor_type = db.relationship( 'SensorType' )
  location = db.relationship( 'Location' )

  @staticmethod
  def create_from_string(k, v): # create measurement from key and value strings
    assert isinstance(k,str), "Key argument must be of type str"
    assert isinstance(v,str), "Value argument must be of type str"

    measurement_type = SensorType.query.filter_by(name=k).first() # find the correct measurement type
    
    if measurement_type == None:
      measurement_type = SensorType(name=k)
    
    return Measurment(sensor_type=measurement_type,value=v)
    


class Station(db.Model):
  id = db.Column( db.Integer , primary_key = True )
  name = db.Column( db.String )
  address = db.Column( db.String )
  locations = db.relationship('Location')
  measurements = db.relationship('Measurment', secondary='location' )

  def read_all(self):
    try:
      req = requests.get(self.address)
      data = req.json() # Convert data to json
      
      assert isinstance( data, dict ), "Data is not in the correct format"
      assert 'locations' in data, "Missing location data from station"
      assert isinstance( data['locations'], list ), "Locations should be of type list"
      
      print(data) # print info for debugging
      
      for location in data['locations']:
        assert 'name' in location, 'Location data must have a name!'
        assert 'data' in location, 'Location data must have a data key!'

        print("Parsing location: ", location['name'])
        print("Using the following measurement types:", str( location['data'].keys() ))

        # self.locations.append(location)
        

    except AssertionError:
      print("Encountered error while requesting data: malformed response" )
    except ConnectionError:
      print("Unable to connect to station at: " + self.address )
    

  
class Location(db.Model):
  id = db.Column( db.Integer , primary_key = True )
  name = db.Column( db.String )
  sation_id = db.Column( db.Integer, db.ForeignKey('station.id'), nullable = False )

  measurments = db.relationship('Measurment')
  station = db.relationship('Station')
