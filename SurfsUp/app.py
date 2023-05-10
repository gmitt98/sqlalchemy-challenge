# Import the dependencies.
import os
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask

#################################################
# Database Setup
#################################################

# create engine to hawaii.sqlite - here i am re-using notebook code from climate_starter
cwd = os.getcwd()
parent_dir = os.path.abspath(os.path.join(cwd, os.pardir))
print(parent_dir)
dbpath = f"{parent_dir}/sqlalchemy-challenge/Resources/hawaii.sqlite"

# reflect an existing database into a new model

engine = create_engine(f"sqlite:///{dbpath}")

print(dbpath)

Base = automap_base()
Base.prepare(engine, reflect=True)

# reflect the tables

Base = automap_base()

# Save references to each table

measurement = Base.classes.measurement
station = Base.classes.station

# Create our session (link) from Python to the DB

session = Session(engine)
'''
#################################################
# Flask Setup
#################################################

App = Flask(__name__)

#################################################
# Flask Routes
#################################################

@app.route("/")
def welcome():
    return(
        "Available API Routes:"

    )

    '''
'''
if __name__ == '__main__':
    app.run(debug=True)
'''
