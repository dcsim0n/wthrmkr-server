# WTHR MKR = Weather Maker
Weather for the Maker in all of us

## Models
+ **Client**: Connects to server and dispalys data ( View )
+ **Server**: Pulls data from stations and stores it over time
+ **Station**: provides interface to location based sensors
+ **Location**: collection of sensors or sensor that is unique to a specific point of interest
+ **Sensor**: device wich provides measurable data about the current weather conditions



## Data

Data from a station might look like this
```python

data = {"locations": 
  [
    { 
      "name": "kitchen", 
      data: [
        { "type": "temperature", "value": "85.2" },
        { "type": "humidity", "value": "62.0" },
        { "type": "wind_speed", "value": "0" }
      ]
    },
    { 
      "name": "patio", 
      data: [
        { "type": "temperature", "value": "90.2" },
        { "type": "humidity", "value": "72.0" },
        { "type": "wind_speed", "value": "10" }
      ]
    }
  ] 
```


## Model Heirarchy

**Sensor names must be unique**

Sensor class would be abstract

Station Model
    |
    V
Location Model
    |
    V
[ Concrete Sensor..] <-- Abstract Sensor class
    |
    V
[ Concrete Service Model.. ] <-- Abstract Service class


## Model Interfaces

Sation
+ Has one or many Locations
+ Returns data to the Server

Location
+ groups related Sensors together
+ fills requests for related data from the Station

Concrete Sensors
+ implemention for specific hardware 
+ inherits from a common Abstract Sensor parent 

Concrete Service
+ implementation for specific measurment types ( temperature, wind speed, humidity )
+ inherits from a common Abstract Service parent

