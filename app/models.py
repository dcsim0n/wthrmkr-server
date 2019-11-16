#!/usr/bin/env python

#-------------------------------------
# WTHR-MKR data modles
# Tim Walter and Dana simmons
#-------------------------------------

from app import db
from sqlalchemy.ext.associationproxy import association_proxy
import requests

class SensorType( db.Model):
  id = db.Column( db.Integer , primary_key = True )
  name = db.Column( db.String )
  measurments = db.relationship('Measurment')

  def get_or_create(cls, **kwargs):
    typ = db.session.query(cls).filter_by(**kwargs).one()
    if typ == None:
      typ = cls(**kwargs)
      db.session.add(cls)
    
    return typ

class Measurment(db.Model):
  id = db.Column( db.Integer, primary_key = True )
  value = db.Column( db.Float )
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
  locations_by_name = association_proxy('locations','name') # create association proxy for locations

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
        loc = Location.get_or_create(name=location['name'])
        print("Found location: ", str(loc))
        self.locations.append(loc) # Will this create duplicate locations?
        print("Using the following measurement types:", str( location['data'].keys() ))

        for measurment in location['data'].keys():
          if measurment == 'timestamp':
            continue
          loc.measurement_from_string( measurment, str(location['data'][measurment]) )

      print( str( self.measurements ))
      db.session.commit()
    except AssertionError:
      print("Encountered error while requesting data: malformed response" )
    except ConnectionError:
      print("Unable to connect to station at: " + self.address )
    

  
class Location(db.Model):
  def __init__(self, name: str): #Allow locations to be created with a string argument
    self.name = name

  id = db.Column( db.Integer , primary_key = True )
  name = db.Column( db.String )
  sation_id = db.Column( db.Integer, db.ForeignKey('station.id'), nullable = False )

  measurments = db.relationship('Measurment')
  station = db.relationship('Station')
  
  @classmethod
  def get_or_create(cls, **kwargs):
    loc = db.session.query(cls).filter_by(**kwargs).one()
    if loc == None:
      loc = cls(**kwargs)
      db.session.add(cls)
    
    return loc

  def measurement_from_string(self, s_type, value): # create measurement from key and value strings
    assert isinstance(s_type,str), "Key argument must be of type str"
    assert isinstance(value,str), "Value argument must be of type str"
    

    measurement_type = SensorType.query.filter_by( name = s_type ).first() # find the correct measurement type
    
    if measurement_type == None:
      measurement_type = SensorType( name = s_type )
    new_measure = Measurment(sensor_type = measurement_type,value = float( value ), location = self)
    self.measurments.append( new_measure )
    return new_measure
