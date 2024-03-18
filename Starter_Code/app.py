# Import the dependencies.
import datetime as dt
import numpy as np
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify
from sqlalchemy import Date
from datetime import datetime, timedelta

#################################################
# Database Setup
#################################################
#create engine
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)
Base.classes.keys()

# Save references to each table
measurement = Base.classes.measurement
Station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)

#################################################
# Flask Setup
#################################################
#create app
app = Flask(__name__)


#################################################
# Flask Routes
#################################################
#define routes
@app.route("/")
def welcome():
    return(
        '''
        Welcome to the Climate App</a><br/>
        /api/v1.0/precipitation</a><br/>
        /api/v1.0/stations</a><br/>
        /api/v1.0/tobs</a><br/>
        /api/v1.0/start_date</a><br/> 
        /api/v1.0/start_date/end_date</a><br/> 
        '''
    )

#create precipitation app
@app.route("/api/v1.0/precipitation")
def precipitation():
    #query precipitation data
    precipitation_data = session.query(measurement.date, measurement.prcp).\
        filter(measurement.date >= "2016-08-24").\
        filter(measurement.date <= "2017-08-23").all()

    session.close()
    #convert the query results into a dictionary
    precipitation_data = {date: prcp for date, prcp in precipitation_data}

    #jsonify results
    return jsonify(precipitation_data)

#create stations app
@app.route("/api/v1.0/stations")
def stations():
    #query stations
    station_results = session.query(measurement.station).all()

    session.close()

    #convert results into list of dictionaries
    station_list = [{"station": station} for station, in station_results]

    #jsonify results
    return jsonify(station_list)

#create tobs app
@app.route("/api/v1.0/tobs")
def tobs():
    #query most active station
    end_date = datetime.strptime("2017-08-23", "%Y-%m-%d")
    start_date = end_date - timedelta(days=365)
    active_station = session.query(measurement.station).\
        group_by(measurement.station).\
        order_by(func.count().desc()).first()[0]
    
    #calculate past year
    last_date = session.query(measurement.date).order_by(measurement.date.desc()).first()[0]
    one_year_ago = datetime.strptime('2017-08-23', '%Y-%m-%d') - timedelta(days=365)

    #query most active stations of previous year
    most_active_station = session.query(measurement.date, measurement.tobs).\
        filter(measurement.station == active_station).\
        filter(measurement.date >= start_date).\
        filter(measurement.date <= end_date).all()

    session.close()

    #convert result in dictionary
    tobs_data = [{"date": date, "tobs": tobs} for date, tobs in most_active_station]

    #jsonify results
    return jsonify(tobs_data)

if __name__ == '__main__':
    app.run(debug=True)