# Python SQL toolkit and Object Relational Mapper
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
import os

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
measurement = Base.classes.measurement
station = Base.classes.station
# Create our session (link) from Python to the DB
session = Session(engine)





from flask import Flask

# starating the flask app

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
def hello4(): # define the function to start
    session = session(Engine) # start our session
    result = session.execute('select station, name, lat, lon, elevation from stations')
    session.close()
    stations = []
    for station,name,lat,lon,elevation in result:
        station_dict = {}
        station_dict["Station"] = station
        station_dict["Name"] = name
        station_dict["Lat"] = lat
        station_dict["Lon"] = lon
        station_dict["Elevation"] = elevation
        stations.append(station_dict)
    return jsonify(stations)

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

