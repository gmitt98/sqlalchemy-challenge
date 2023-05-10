# Python SQL toolkit and Object Relational Mapper
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
import os
from flask import Flask
from flask import jsonify

# all the things to set up the database connection

# create engine to hawaii.sqlite
cwd = os.getcwd()
parent_dir = os.path.abspath(os.path.join(cwd, os.pardir))
print(parent_dir)
dbpath = f"{parent_dir}/sqlalchemy-challenge/Resources/hawaii.sqlite" # for some reason i had to add one more folder level
engine = create_engine(f"sqlite:///{dbpath}")
print(dbpath)
# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)
# Save references to each table
print(Base.classes.keys())
Measurement = Base.classes.measurement
Station = Base.classes.station


from flask import Flask

# starting the flask app

app = Flask(__name__)

# all routes listed in simple return

@app.route("/")
def hello():
    # routes available
    return (
        f"API Routes:<br/>"
        f"Precipitation: /api/v1.0/precipitation<br/>"
        f"Stations: /api/v1.0/stations<br/>"
        f"1yr Temp: /api/v1.0/tobs<br/>"
        f"Temp since date (format: yyyy-mm-dd): /api/v1.0/yyyy-mm-dd<br/>"
        f"Temp between two dates(format: yyyy-mm-dd): /api/v1.0/yyyy-mm-dd/yyyy-mm-dd"
    )

@app.route('/api/v1.0/hello')
def hello2():
    return 'Hello, World!'

@app.route('/api/v1.0/precipitation')
def hello3(): 

    return 'Hello, World!'

@app.route('/api/v1.0/stations') # this will return a list of stations when called
def get_stations():
    session = Session(engine) # connect to the database
    results = session.query(Station.station, Station.name, Station.latitude, Station.longitude, Station.elevation).all() # get these data for all rows in teh table, returning it as a list of tuples
    session.close()
    stations = [] # open a list that i will put my dictionaries into
    for station, name, latitude, longitude, elevation in results: # iterate through the list of tuples
        station_dict = {} # for each item in the list of tuples, create a dictionary, and then we will drop the items in there
        station_dict['station'] = station
        station_dict['name'] = name
        station_dict['latitude'] = latitude
        station_dict['longitude'] = longitude
        station_dict['elevation'] = elevation
        stations.append(station_dict) # add this dict to my list of dicts
    return jsonify(stations) # jsonify the final result which returns my json object request respose for this route


@app.route('/api/v1.0/tobs')
def hello5():
    return 'Hello, World!'

@app.route('/api/v1.0/<start>')
def hello6():
    return 'Hello, World!'

@app.route('/api/v1.0/<start>/<end>')
def hello7():
    return 'Hello, World!'


# running the code with debugger on
if __name__ == '__main__':
    app.run(debug=True)

