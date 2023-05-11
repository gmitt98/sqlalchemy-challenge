# Python SQL toolkit and Object Relational Mapper
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
import os
from flask import Flask
from flask import jsonify
from datetime import datetime
from datetime import timedelta

# all the things to set up the database connection

# create engine to hawaii.sqlite
cwd = os.getcwd()
parent_dir = os.path.abspath(os.path.join(cwd, os.pardir))
print(parent_dir)
dbpath = f"{parent_dir}/sqlalchemy-challenge/Resources/hawaii.sqlite" # for some reason i had to add one more folder level
print(dbpath)
engine = create_engine(f"sqlite:///{dbpath}")
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

@app.route('/api/v1.0/precipitation') # dropping in the code i had in the notebook
def get_precipitation():
    session = Session(engine)
    max_date_query = session.execute('SELECT MAX(date) FROM measurement')
    for row in max_date_query:
        max_date_string = row[0]
        print(max_date_string)
    max_date = datetime.strptime(max_date_string, '%Y-%m-%d').date()
    one_year_ago = max_date - timedelta(days=365)
    print(one_year_ago)
    query = 'select date, prcp from measurement where date > :one_year_ago'
    result = session.execute(query, {'one_year_ago':one_year_ago})
    prcp_list = [] # now i write the results out: row -> dict -> list -> json object -> return
    for date, prcp in result:
        prcp_dict = {}
        prcp_dict['date'] = date
        prcp_dict['prcp'] = prcp
        prcp_list.append(prcp_dict)
    return jsonify(prcp_list)

@app.route('/api/v1.0/stations')
def get_stations():
    session = Session(engine)
    result = session.execute('SELECT id, station, name, latitude, longitude, elevation FROM station')
    stations = []
    for id, station, name, latitude, longitude, elevation in result:
        station_dict = {}
        station_dict['id'] = id
        station_dict['station'] = station
        station_dict['name'] = name
        station_dict['latitude'] = latitude
        station_dict['longitude'] = longitude
        station_dict['elevation'] = elevation
        stations.append(station_dict)
    session.close()
    return jsonify(stations)

@app.route('/api/v1.0/stations2')
def get_stations2():
    session = Session(engine) # connect to the database
    results = session.execute('SELECT id, station, name, latitude, longitude, elevation FROM station').fetchall() # get these data for all rows in the table, returning it as a list of tuples
    session.close()
    stations = [] # open a list that i will put my dictionaries into
    for id, station, name, latitude, longitude, elevation in results: # iterate through the list of tuples
        station_dict = {} # for each item in the list of tuples, create a dictionary, and then we will drop the items in there
        station_dict['id'] = id
        station_dict['station'] = station
        station_dict['name'] = name
        station_dict['latitude'] = latitude
        station_dict['longitude'] = longitude
        station_dict['elevation'] = elevation
        stations.append(station_dict) # add this dict to my list of dicts
    return jsonify(stations) # jsonify the final result which returns my json object request respose for this route

@app.route('/api/v1.0/stations3') # this will return a list of stations when called
def get_stations3():
    session = Session(engine) # connect to the database
    results = session.query(Station.id, Station.station, Station.name, Station.latitude, Station.longitude, Station.elevation).all() # get these data for all rows in teh table, returning it as a list of tuples
    session.close()
    stations = [] # open a list that i will put my dictionaries into
    for id, station, name, latitude, longitude, elevation in results: # iterate through the list of tuples
        station_dict = {} # for each item in the list of tuples, create a dictionary, and then we will drop the items in there
        station_dict['id'] = id
        station_dict['station'] = station
        station_dict['name'] = name
        station_dict['latitude'] = latitude
        station_dict['longitude'] = longitude
        station_dict['elevation'] = elevation
        stations.append(station_dict) # add this dict to my list of dicts
    return jsonify(stations) # jsonify the final result which returns my json object request respose for this route


@app.route('/api/v1.0/tobs')
def get_tobs():
    session = Session(engine)
    max_date_query = session.execute('SELECT MAX(date) FROM measurement')
    for row in max_date_query:
        max_date_string = row[0]
    max_date = datetime.strptime(max_date_string, '%Y-%m-%d').date()
    one_year_ago = max_date - timedelta(days=365)
    station_activity_result = session.execute('select station, count(id) as count_id from measurement group by station order by count_id desc')
    station_activity_result_list = []
    for row in station_activity_result:
        station_activity_result_list.append(row)
    most_active_station_name = station_activity_result_list[0][0]
    query = 'select date, tobs from measurement where station = :most_active_station_name and date >= :one_year_ago'
    most_active_data_query_hist = session.execute(query, {'most_active_station_name':most_active_station_name, 'one_year_ago':one_year_ago})
    most_active_data_dict_list = [] # I will write the data to a dictionary
    for row in most_active_data_query_hist:
        most_active_data_dict_list.append({'date': row[0], 'tobs': row[1]})
    return jsonify(most_active_data_dict_list)

@app.route('/api/v1.0/<start>') # <start> is the variable part of the route url
def get_start(start):
    session = Session(engine)
    query = 'SELECT MIN(tobs), AVG(tobs), MAX(tobs) FROM measurement WHERE date >= :start'
    start_stats = session.execute(query, {'start':start})
    start_stats_dict_list = []
    for min_temp, avg_temp, max_temp in start_stats:
        start_stats_dict = {}
        start_stats_dict['min_temp'] = min_temp
        start_stats_dict['avg_temp'] = round(avg_temp,1)
        start_stats_dict['max_temp'] = max_temp
        start_stats_dict_list.append(start_stats_dict)
    return jsonify(start_stats_dict_list)

@app.route('/api/v1.0/<start>/<end>') # <start> is the first variable of the route url and <end> is the second
def get_start_end(start,end):
    session = Session(engine)
    query = 'SELECT MIN(tobs), AVG(tobs), MAX(tobs) FROM measurement WHERE date >= :start and date <= :end'
    start_end_stats = session.execute(query, {'start':start, 'end':end})
    start_end_stats_dict_list = []
    for min_temp, avg_temp, max_temp in start_end_stats:
        start_end_stats_dict = {}
        start_end_stats_dict['min_temp'] = min_temp
        start_end_stats_dict['avg_temp'] = round(avg_temp,1)
        start_end_stats_dict['max_temp'] = max_temp
        start_end_stats_dict_list.append(start_end_stats_dict)
    return jsonify(start_end_stats_dict_list)

# running the code with debugger on
if __name__ == '__main__':
    app.run(debug=True)