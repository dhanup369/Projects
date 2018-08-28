import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)


#################################################
# Flask Routes
#################################################

@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/start_date<br/>"
        f"/api/v1.0/start_end_date"
    )


@app.route("/api/v1.0/precipitation")
def precipitation():
    """Return a list of all passenger names"""
    # Query all precipitation data
    results=session.query(Measurement.date, Measurement.prcp).filter(Measurement.date > '2016-08-23').all()
    prcp_list=[]
    for i in results:
        prcp_dict={}
        prcp_dict['date']=i.date
        prcp_dict['prcp']=i.prcp
        prcp_list.append(prcp_dict)
    return jsonify(prcp_list)

@app.route("/api/v1.0/stations")
def stations():
    """Return a list of stations"""
    # Query all stations
    results = session.query(Measurement.station).group_by(Measurement.station).all()
    return jsonify(results)

@app.route("/api/v1.0/tobs")
def tobs():    
    results=session.query(Measurement.date, Measurement.tobs).filter(Measurement.date > '2016-08-23').all()
    tobs_list=[]
    for i in results:
        tobs_dict={}
        tobs_dict['date']=i.date
        tobs_dict['tobs']=i.tobs
        tobs_list.append(tobs_dict)
    return jsonify(tobs_list)

@app.route("/api/v1.0/start_date/<start>")
def start_date(start):
        results=session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs),func.max(Measurement.tobs)).filter(Measurement.date>=start).all()                                     
        return jsonify(results)

@app.route("/api/v1.0/start_end_date/<start>,<end>")
def start_end_date(start,end):
        results=session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs),func.max(Measurement.tobs)).filter(Measurement.date>=start).filter(Measurement.date<end).all()                                     
        return jsonify(results)

if __name__ == '__main__':
    app.run(debug=True)


