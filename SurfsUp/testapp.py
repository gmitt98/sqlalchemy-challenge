# Python SQL toolkit and Object Relational Mapper
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
import os
# create engine to hawaii.sqlite
cwd = os.getcwd()
parent_dir = os.path.abspath(os.path.join(cwd, os.pardir))
print(parent_dir)
dbpath = f"{parent_dir}/sqlalchemy-challenge/Resources/hawaii.sqlite"
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

app = Flask(__name__)


@app.route("/")
def hello():
    # routes available
    return (
        f"API Routes:<br/>"
        f"Precipitation: /api/v1.0/precipitation<br/>"
        f"Stations: /api/v1.0/stations<br/>"
        f"1yr Temp: /api/v1.0/tobs<br/>"
        f"Temp since date(yyyy-mm-dd): /api/v1.0/yyyy-mm-dd<br/>"
        f"Temp between two dates(yyyy-mm-dd): /api/v1.0/yyyy-mm-dd/yyyy-mm-dd"
    )

@app.route('api/v1.0/hello')
def hello2():
    return 'Hello, World!'

@app.route('api/v1.0/precipitation')
def hello3():
    return 'Hello, World!'

@app.route('api/v1.0/stations')
def hello4():
    return 'Hello, World!'

@app.route('api/v1.0/tobs')
def hello5():
    return 'Hello, World!'

@app.route('api/v1.0/<start>')
def hello6():
    return 'Hello, World!'

@app.route('api/v1.0/<start>/<end>')
def hello7():
    return 'Hello, World!'

if __name__ == '__main__':
    app.run(debug=True)

