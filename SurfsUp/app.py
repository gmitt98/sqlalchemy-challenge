#################################################
# Import Dependencies
#################################################

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
import os
from flask import Flask
from flask import jsonify
from datetime import datetime
from datetime import timedelta

#################################################
# Set Up Database Connection
#################################################

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

#################################################
# Start Flask
#################################################

app = Flask(__name__)

#################################################
# Flask Routes
#################################################

# all routes listed in simple return
@app.route("/")
def hello():
    # routes available
    return (
        f"API Routes:<br/>"
        f"Last 1yr Precipitation: /api/v1.0/precipitation<br/>"
        f"Stations: /api/v1.0/stations<br/>"
        f"Last 1yr Temp stats: /api/v1.0/tobs<br/>"
        f"Temp stats since date (format: yyyy-mm-dd): /api/v1.0/yyyy-mm-dd<br/>"
        f"Temp stats between two dates(format: yyyy-mm-dd): /api/v1.0/yyyy-mm-dd/yyyy-mm-dd"
    )

# precipitation route: reuse notebook code, return all precipitation from 1 year ago
@app.route('/api/v1.0/precipitation') # dropping in (mostly) the code i had in the notebook. i renamed some result vars in order to read it more cleanly here.
def get_precipitation():
    session = Session(engine)
    # get the latest date in the data
    max_date_query = session.execute('SELECT MAX(date) FROM measurement')
    for row in max_date_query:
        max_date_string = row[0]
        print(max_date_string)
    max_date = datetime.strptime(max_date_string, '%Y-%m-%d').date()
    #find the date one year prior to latest date in the data
    one_year_ago = max_date - timedelta(days=365)
    print(one_year_ago)
    # define and run my query
    prcp_query = 'SELECT date, prcp FROM measurement WHERE date >= :one_year_ago'
    prcp_result = session.execute(prcp_query, {'one_year_ago':one_year_ago})
    # now i write the results out: row -> dicts -> list of dicts -> json object -> return. this will be done on all routes
    prcp_list = [] 
    for date, prcp in prcp_result:
        prcp_dict = {}
        prcp_dict[f'{date}'] = prcp
        prcp_list.append(prcp_dict)
    session.close()
    return jsonify(prcp_list)

# return the stations information
@app.route('/api/v1.0/stations')
def get_stations():
    session = Session(engine)
    station_result = session.execute('SELECT id, station, name, latitude, longitude, elevation FROM station')
    stations = []
    # i will write the data to a dictionary then return it as json
    for id, station, name, latitude, longitude, elevation in station_result:
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

# observed temp information
@app.route('/api/v1.0/tobs')
def get_tobs():
    session = Session(engine)
    # reusing notebook code to get date for start of the last year in the data
    max_date_query = session.execute('SELECT MAX(date) FROM measurement')
    for row in max_date_query:
        max_date_string = row[0]
    max_date = datetime.strptime(max_date_string, '%Y-%m-%d').date()
    one_year_ago = max_date - timedelta(days=365)
    # reusing notebook code to get the most active station name
    station_activity_result = session.execute('SELECT station, count(id) AS count_id FROM measurement GROUP BY station ORDER BY count_id desc')
    station_activity_result_list = []
    for row in station_activity_result:
        station_activity_result_list.append(row)
    most_active_station_name = station_activity_result_list[0][0]
    # building the query to get the history for that specific station
    #query as a string i'll pass things into - f-strings in the query gave me trouble so i didn't do it
    query = 'SELECT date, tobs FROM measurement WHERE station = :most_active_station_name AND date >= :one_year_ago'
    # i found this approach to passing variables in to my query to work.
    most_active_data_query_hist = session.execute(query, {'most_active_station_name':most_active_station_name, 'one_year_ago':one_year_ago}) 
    most_active_data_dict_list = [] 
    # i will write the data to a dictionary then return it as json
    for row in most_active_data_query_hist:
        most_active_data_dict_list.append({'date': row[0], 'tobs': row[1]})
    session.close()
    return jsonify(most_active_data_dict_list)

# stats from a given date to the end of the data available. note: the instructions didn't specify to filter this to a single station, so i didn't
@app.route('/api/v1.0/<start>') # <start> is the variable part of the route url
def get_start(start): # passing start into this function
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
    session.close()
    return jsonify(start_stats_dict_list)

# date range route. note: the instructions didn't specify to filter this to a single station, so i didn't
@app.route('/api/v1.0/<start>/<end>') # <start> is the first variable of the route url and <end> is the second
def get_start_end(start,end): #passing start and end into this function
    session = Session(engine)
    query = 'SELECT MIN(tobs), AVG(tobs), MAX(tobs) FROM measurement WHERE date >= :start AND date <= :end'
    start_end_stats = session.execute(query, {'start':start, 'end':end})
    start_end_stats_dict_list = []
    # i will write the data to a dictionary then return it as json
    for min_temp, avg_temp, max_temp in start_end_stats:
        start_end_stats_dict = {}
        start_end_stats_dict['min_temp'] = min_temp
        start_end_stats_dict['avg_temp'] = round(avg_temp,1)
        start_end_stats_dict['max_temp'] = max_temp
        start_end_stats_dict_list.append(start_end_stats_dict)
    session.close()
    return jsonify(start_end_stats_dict_list)

# running the code with debugger on
if __name__ == '__main__':
    app.run(debug=True)