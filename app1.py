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

@app.route("/api/v1.0/<start>")
def startDate():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Enter the start date
    Start_date = dt(input("Enter a start date:"))

    query_date = Start_date

    # Query the temperature observation data for the given date
    results = session.query(func.min(Measurement.tobs), func.max(Measurement.tobs),func.avg(Measurement.tobs))\
                            .filter(Measurement.date >= query_date).all()

    session.close()

    # Create a dictionary from the row data and append to a list of all_precipitation
    all_tempObs2 = []
    for result in results:
        temp2_dict = {}
        temp2_dict["Min Temperature"] = result[0]
        temp2_dict["Max temperature"] = result[1]
        temp2_dict["Avg temperature"] = result[2]
        
        all_tempObs2.append(temp2_dict)

    return jsonify(all_tempObs2)


#     # Convert list of tuples into normal list
#     all_names = list(np.ravel(results))

#     return jsonify(all_names)

# @app.route("/api/v1.0/pets")
# def pets():
#     # Create our session (link) from Python to the DB
#     session = Session(engine)

#     """Return a list of pet data including the name, type, and age of each pet"""
#     # Query all pets
#     results = session.query(Pet.name, Pet.age, Pet.type).all()

#     session.close()

#     # Create a dictionary from the row data and append to a list of all_passengers
#     all_pets = []
#     for name, age, type in results:
#         pet_dict = {}
#         pet_dict["name"] = name
#         pet_dict["age"] = age
#         pet_dict["type"] = type
#         all_pets.append(pet_dict)

#     return jsonify(all_pets)

#################################################
if __name__ == '__main__':
    app.run(debug=True)