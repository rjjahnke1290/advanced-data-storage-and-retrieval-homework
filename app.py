

# We import dependencies from SQLAlchemy and Flask.
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

# This creates an engine based on our sqlite file, and makes a connection thereto.
engine = create_engine("sqlite:///Data/hawaii.sqlite?check_same_thread=False")
conn = engine.connect()

 # This reflects an existing database into a new model.
Base = automap_base()

# This reflects the tables of the database.
Base.prepare(engine, reflect=True)

# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

# This creates a session (or a link) from Python to the database.
session = Session(engine)

# This creates an app
# We must be sure to pass __name__
app = Flask(__name__)

# This defines what to do when a user hits the index route
@app.route("/")
def home():
    return (
    "Welcome to my weather data page!</br></br>"
    "Available directories</br>"
    "/api/v1.0/precipitation</br>"
    "/api/v1.0/stations</br>"
    "/api/v1.0/tobs</br></br>"
    "The following links depend on user input.  Please replace &lt;start_date&gt; and &lt;end_date&gt; with a date in the format YYYY-MM-DD</br>"
    "/api/v1.0/&lt;start_date&gt;</br>"
    "/api/v1.0/&lt;end_date&gt;</br>"
    "/api/v1.0/&lt;start_date&gt;/&lt;end_date&gt;")

@app.route("/api/v1.0/precipitation")
def precipitation():
    # This queries the columns date and (prcp) precipitation from the table Measurement for the final year of our data.
    date_precipitation_final_year = session.query(Measurement.date, Measurement.prcp) \
    .filter(Measurement.date.between("2016-08-23", "2017-08-23"))

    # We now save the query results into a dictionary using date as the key and prcp as the value.
    date_precipitation__final_year_dictionary = {date : prcp for date, prcp in date_precipitation_final_year}

    # We can now return our query results as a JSON.
    return jsonify(date_precipitation__final_year_dictionary)

@app.route("/api/v1.0/stations")
def stations():
    # This queries the column station from the table Station
    stations = session.query(Station.station)
    
    # We now save the query results into a list.
    stations_list = [station for station in stations]

    # We can now return our query results as a JSON.
    return jsonify(stations_list)

@app.route("/api/v1.0/tobs")
def tobs():
    # This queries the  columns date and tobs (temperature observations) from the table Measurement for the final year of our data.
    dates_temperatures_final_year = session.query(Measurement.date, Measurement.tobs).filter(func.strftime("%Y-%m-%d", Measurement.date) >= "2016-08-23").filter(func.strftime("%Y-%m-%d", Measurement.date) <= "2017-08-23").all()

    # We now save the query results into a list.
    dates_temperatures__final_year_dictionary = [temperature for date, temperature in dates_temperatures_final_year]

    # We can now return our query results as a JSON.
    return jsonify(dates_temperatures__final_year_dictionary)



"""The following two routes return a JSON of the minimum, maximum, and average temperature between two dates.  In the first route, the user defines the start date, and the JSON returns the respective temperatures from that date until the final date in our data (2017-08-23).  In the second route, the user defines both the start date and the end date, and the JSON returns the respective temperatures between the two dates given.

In both routes, we query the minimum, maximum, and average temperature, from the table Measurement.  In the first route, we filter the query to only dates greater than or equal to the date given.  In the second route, we filter the query to only dates between the two dates given.  In both queries, we return the query results as a JSON."""

@app.route("/api/v1.0/<start_date>")
def start(start_date):
    min_max_avg_from_start = session.query(func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs)).filter(func.strftime("%Y-%m-%d", Measurement.date) >= start_date).filter(func.strftime("%Y-%m-%d", Measurement.date) <= "2017-08-23").all()

    return jsonify(min_max_avg_from_start)

# @app.route("/api/v1.0/<end_date>")
# def start(end_date):
#     min_max_avg_until_end = session.query(func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs)).filter(func.strftime("%Y-%m-%d", Measurement.date) >= "2010-01-01").filter(func.strftime("%Y-%m-%d", Measurement.date) <= end_date).all()

#     return jsonify(min_max_avg_until_end)

@app.route("/api/v1.0/<start_date>/<end_date>")
def start_end(start_date, end_date):
    min_max_avg_between_two_dates = session.query(func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs)).filter(func.strftime("%Y-%m-%d", Measurement.date) >= start_date).filter(func.strftime("%Y-%m-%d", Measurement.date) <= end_date).all()
   
    return jsonify(min_max_avg_between_two_dates)

if __name__ == "__main__":
    app.run(debug=True)
