import numpy as np
import datetime as dt

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify


#################################################
# Database Setup
#################################################
engine = create_engine(f"sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
Measurement = Base.classes.measurement
Station = Base.classes.station

#################################################
# Flask Setup
#################################################
app = Flask(__name__)


#################################################
# Flask Routes
#################################################

# /
# Homepage.
# List all available routes.

@app.route("/")
def Homepage():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end>"

    )

# /api/v1.0/precipitation
# Convert the query results to a dictionary using date as the key and prcp as the value.
# Return the JSON representation of your dictionary.    

@app.route("/api/v1.0/precipitation")
def datesAndprcp():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Convert the query results to a dictionary using date as the key and prcp as the value"""
    # Find the most recent date in the data set.
    RecentDate = session.query(func.max(Measurement.date)).all()

    # Calculate the date one year from the last date in data set.
    query_date = dt.date(2017, 8, 23) - dt.timedelta(days=365)

    # Perform a query to retrieve the data and precipitation scores
    results = session.query(Measurement.date, Measurement.prcp)\
                                .filter(Measurement.date > query_date).all()

    session.close()

    # Create a dictionary from the row data and append to a list of all_precipitation
    all_precipitation = []
    for date, prcp in results:
        precipitation_dict = {}
        precipitation_dict["Date"] = date
        precipitation_dict["PRCP"] = prcp
        
        all_precipitation.append(precipitation_dict)

    return jsonify(all_precipitation)

# /api/v1.0/stations
# Return a JSON list of stations from the dataset.

@app.route("/api/v1.0/stations")
def Stations():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of all Stations"""
    # Query all pets
    results = session.query(Station.station).all()

    session.close()

    # Convert list of tuples into normal list
    all_stations = list(np.ravel(results))

    return jsonify(all_stations)

#/api/v1.0/tobs
# Query the dates and temperature observations of the most active station for the previous year of data.
# Return a JSON list of temperature observations (TOBS) for the previous year.

@app.route("/api/v1.0/tobs")
def TempObservations():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Convert the query results to a dictionary using date as the key and tempObs as the value"""
    # Find the most recent date in the data set for the most active station.
    RecentDate_station = session.query(func.max(Measurement.date)).filter_by(station = "USC00519281").all()

    # Calculate the date one year from the last date in data set.
    query_date = dt.date(2017, 8, 18) - dt.timedelta(days=365)

    # Query the last 12 months of temperature observation data for this station
    results = session.query(Measurement.date, Measurement.tobs)\
                            .filter(Measurement.date > query_date)\
                            .filter_by(station = "USC00519281").all()

    session.close()

    # Create a dictionary from the row data and append to a list of all_precipitation
    all_tempObs = []
    for date, tobs in results:
        temp_dict = {}
        temp_dict["Date"] = date
        temp_dict["TOBS"] = tobs
        
        all_tempObs.append(temp_dict)

    return jsonify(all_tempObs)

# /api/v1.0/<start> and /api/v1.0/<start>/<end>
# Return a JSON list of the minimum temperature, the average temperature, and the maximum temperature for a given start or start-end range.
# When given the start only, calculate TMIN, TAVG, and TMAX for all dates greater than or equal to the start date.
# When given the start and the end date, calculate the TMIN, TAVG, and TMAX for dates from the start date through the end date (inclusive).

@app.route("/api/v1.0/<start>")
def startDate(start):
    # Create our session (link) from Python to the DB
    session = Session(engine)

    # make a start date variable
    Start_date = dt.datetime.strptime(start,"%Y-%m-%d")

    results = session.query(func.min(Measurement.tobs), func.max(Measurement.tobs),func.avg(Measurement.tobs))\
                            .filter(Measurement.date >= Start_date).all()

    session.close()

    # Create a dictionary from the row data and append to a list of all_TOBS from the start date 
    all_TOBS_start_date = []
    for result in results:
         temp2_dict = {}
         temp2_dict["Min Temperature"] = result[0]
         temp2_dict["Max temperature"] = result[1]
         temp2_dict["Avg temperature"] = result[2]
        
    all_TOBS_start_date.append(temp2_dict)

    return jsonify(all_TOBS_start_date)

@app.route("/api/v1.0/<start>/<end>")
def start_end_dates(start, end):
    # Create our session (link) from Python to the DB
    session = Session(engine)
    # Query the avg, min and max temp
    results = session.query(func.avg(Measurement.tobs), func.min(Measurement.tobs), func.max(Measurement.tobs))\
                            .filter(Measurement.date >= start)\
                            .filter(Measurement.date <= end).all()
    # Close session
    session.close()

    # Another way of finding the avg, min and max temps
    # start_and_end = list(np.ravel(results))
    # return jsonify(start_and_end)

    # Create a dictionary from the row data and append to a list of all_TOBS
    all_TOBS = []
    for result in results:
         temp2_dict = {}
         temp2_dict["Avg Temperature"] = result[0]
         temp2_dict["Min temperature"] = result[1]
         temp2_dict["Max temperature"] = result[2]
        
    all_TOBS.append(temp2_dict)

    return jsonify(all_TOBS)

#################################################
if __name__ == '__main__':
    app.run(debug=True, port = 8000)