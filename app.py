# importing necessary libraries
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

# Create connection to our sqlite query
engine = create_engine('sqlite:///hawaii.sqlite?check_same_thread=False')
connect = engine.connection

Base = automap_base()

# Table references
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create session
session = Session(engine)

app = Flask(__name__)

@app.route("/")
def home():
    return (
        'Welcome to my weather data page</br>'
        'Available directories</br>'
        '/api/v1.0/precipitation</br>'
        '/api/v1.0/stations</br>'
        '/api/v1.0/tobs</br></br>'
        'The following links depend on user input.  Please replace &lt;start_date&gt; and &lt;end_date&gt; with a date in the format YYYY-MM-DD</br>'
        '/api/v1.0/&lt;start_date&gt;</br>'
        '/api/v1.0/&lt;end_date&gt;</br>')

@app.route("/api/v1.0/precipitation")
def precipitation():
    # Runs a query for precipitation
    last_year_precip = session.query(Measurement.date, Measurement.prcp) \
    .filter(Measurement.date.between("2016-08-23", "2017-08-23"))

    # Creates dictionary
    last_year_precip_data = {date : prcp for date, prcp in last_year_precip}

    # Return as a json.
    return jsonify(last_year_precip_data)

@app.route("/api/v1.0/stations")
def stations():
    # Runs a query for stations
    stations = session.query(Station.station)

    # Generate a list for the query
    stations_list = [station for station in stations]

    # Return the list as a query
    return jsonify(stations_list)

@app.route("/api/v1.0/tobs")
def tobs():
    # Runs a query for temperatures over last year
    temp_last_year = session.query(Measurement.date, Measurement.tobs)\
                        .filter(func.strftime("%Y-%m-%d", Measurement.date) >= "2016-08-23")\
                        .filter(func.strftime("%Y-%m-%d", Measurement.date) <= "2017-08-23").all()

    # Moves query to a list
    temp_last_year_dict = [temperature for date, temperature in temp_last_year]

    # Returns dictionary as a json
    return jsonify(temp_last_year_dict)

@app.route("/api/v1.0/<start>")
def start(start_date):
    summary_temp = session.query(func.min(Measurement.tobs), \
                    func.max(Measurement.tobs), func.avg(Measurement.tobs))\
                    .filter(func.strftime("%Y-%m-%d", Measurement.date) >= start_date)\
                    .filter(func.strftime("%Y-%m-%d", Measurement.date) <= "2017-08-23").all()

    return jsonify(summary_temp)

@app.route('/api/v1.0/<start>/<end>')
def start_end(start_date, end_date):
    summary_between = session.query(func.min(Measurement.tobs), \
                        func.max(Measurement.tobs), func.avg(Measurement.tobs))\
                        .filter(func.strftime("%Y-%m-%d", Measurement.date) >= start_date)\
                        .filter(func.strftime("%Y-%m-%d", Measurement.date) <= end_date).all()

    return jsonify(summary_between)

if __name__ == '__main__':
    app.run(debug=True)
