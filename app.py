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
