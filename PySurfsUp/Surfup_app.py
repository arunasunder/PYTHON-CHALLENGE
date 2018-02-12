# #################################################
## Ensure to start the flask server and then go to the URL link given at the flask service console 
## The try out the commands 
## Ensure that all the other jpynb files are run 
## 
## Author: Aruna Amaresan 
## 
## LAst Modified: Feb 11th 2018 
###################################################

#Ensure to Import dependencies
import datetime as dt
import numpy as np
import pandas as pd
from time import time
import os
from datetime import datetime, timedelta, date 
import math

import sqlalchemy
from sqlalchemy import and_
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, inspect, func

from flask import Flask, jsonify


#################################################
# Database Setup
#################################################
#Create a path to open the Hawaii SQL Liste DB 
Hawaii_DBPath = os.path.join('Resources', 'hawaii.sqlite')

print (Hawaii_DBPath)

Hawaii_sqlite = 'sqlite:///' + Hawaii_DBPath

print(Hawaii_sqlite)


engine = create_engine(Hawaii_sqlite)

#Inspect the DB info 
inspector = inspect(engine)
print (inspector.get_table_names())

# reflect an existing database into a new model
Base = automap_base()
Base.prepare(engine, reflect=True)

# Save references to the measurement and station tables
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
        f"<h1>Avalable Routes:</h1><br/>"
        f"<h3>/api/v1.0/precipitation - Date and Precipitation Observations From Last year</h3><br/>"

        f"<h3>/api/v1.0/stations"
        f" - List of Stations</h3><br/>"

        f"<h3>/api/v1.0/tobs"
        f" - List of Temperature Observations (tobs) for the previous year</h3><br/>"

        f"<h3>/api/v1.0/&ltstart_date&gt" 
        f" - Return TMIN, TAVG, and TMAX for all dates greater than and equal to the start date.<br>"
        f" - Enter start_date in YYYY-MM-DD format</h3><br/>"

        f"<h3>/api/v1.0/&ltstart_date&gt/&ltend_date&gt"
        f" - Return ITMIN, TAVG, and TMAX for dates between the start and end date inclusive.<br/>"
        f" - Enter start_date and end-date in YYYY-MM-DD format</h3><br/>"
    )


@app.route("/api/v1.0/stations")
def list_stations():
    
    # Query all stations from the Stations table
    #results = session.query(Invoices.BillingCountry).\
    #    group_by(Invoices.BillingCountry).all()

    results2 = session.query(Measurement.station_code).\
            group_by(Measurement.station_code).\
            order_by(func.count(Measurement.station_code).desc()).all()

    print(results2)

    # Convert list of tuples into normal list
    stations_list = list(np.ravel(results2))

    return jsonify(stations_list)


@app.route("/api/v1.0/precipitation")
def precipitation_last_year():
    #Return precipitation for the last year
    # Each item in the list is a dictionary with keys `date` and value as prcp value 
    
    # PRECIPITATION ANALYSIS 
    # =======================
    #Pull Data as per request for the last 12 months info 
    Curr_Date = datetime.today().date()

    print (Curr_Date)
    One_year_ago_date = Curr_Date - timedelta(days=365)
    print(One_year_ago_date)


    results = session.query(Measurement.date, Measurement.prcp).\
                filter(and_(Measurement.date <= Curr_Date, Measurement.date >= One_year_ago_date)).\
                order_by(Measurement.date.desc()).all()

    print (results)

    # Create a list of dicts with `country` and `total` as the keys and
    '''invoice_totals = []

    for result in results:
        row = {}
        row["country"] = result[0]
        row["total"] = float(result[1])
        invoice_totals.append(row) '''

    precp_results = {}
    for result in results:
        #row = {}
        date_str = result[0].strftime("%Y-%m-%d")
        print(date_str)
        precp_val = float(result[1])
        precp_results[date_str] = precp_val
        #precp_results[result[0]].append(result[1])
        #row["Date"] = result[0]
        #row["total"] = float(result[1])

        #row["country"] = result[0]
        #row["total"] = float(result[1])
        #invoice_totals.append(row)

    for key in precp_results.keys():
        val = precp_results[key]
        print("Key: ", str(key), 'points to: ', str(val))

    return jsonify(precp_results)


@app.route("/api/v1.0/tobs")
def temperature_previous_year():
    #Return temperature for the previous year
    # Each item in the list is a dictionary with keys `date` and value as temp value 
    
    # TEMPERTAURE  ANALYSIS 
    # =======================
    #Pull Data as per request for the previous year info 
    datestring = "2017-01-01"
    start_dt = datetime.strptime(datestring, '%Y-%m-%d')

    print(start_dt)

    datestring = "2017-12-31"
    end_dt = datetime.strptime(datestring, '%Y-%m-%d')

    print(end_dt)

    #last_year_End_Date = datetime.date(2017, 12, 31)

    #print(last_year_Start_Date)
    #print(last_year_End_Date)
    # Go back from Temperature on full of last year 
    #previous_year_ago_date = Curr_Date - timedelta(days=365)
    #print(One_year_ago_date)

    results = session.query(Measurement.date, Measurement.tobs).\
                filter(and_(Measurement.date <= end_dt, Measurement.date >= start_dt)).\
                order_by(Measurement.date.desc()).all()

    print (results)

    # Create a list of dicts with `country` and `total` as the keys and
    temp_results = {}
    for result in results:
        #row = {}
        date_str = result[0].strftime("%Y-%m-%d")
        print(date_str)
        temp_val = int(result[1])
        temp_results[date_str] = temp_val


    for key in temp_results.keys():
        val = temp_results[key]
        print("Key: ", str(key), 'points to: ', str(val))

    return jsonify(temp_results)

@app.route("/api/v1.0/<start_date>")
def calc_temp_stats_post_startdate(start_date):
    # Calculate Minimum, Maximum and Average temperature for all observations taken after start date ]
    print(start_date)
    #print(end_date)
    #print (Measurement)
    #Now Run querue to find the Values to plot min max and average temps 
    results = session.query(Measurement.tobs).\
                filter(Measurement.date >= start_date).\
                order_by(Measurement.date.desc()).all()
    
    temp_df = pd.DataFrame(results, columns=['tobs'])
    #temp_df.set_index('date', inplace=True, )
    #print ("Return Dataframe is:")
    #print (temp_df)
    #temp_df.head(10)
    
    min_temp = temp_df['tobs'].min()
    print(min_temp)
    
    max_temp = temp_df['tobs'].max()
    print(max_temp)
    
    avg_temp = temp_df['tobs'].mean()
    print(avg_temp)

    tempsummary_results = {}
    #for result in results:
        #row = {}
        #date_str = result[0].strftime("%Y-%m-%d")
        #print(date_str)
    #temp_val = float(result[0])
    #date_str = start_date.strftime("%Y-%m-%d")
    tempsummary_results['Start_Date'] = str(start_date)
    
    # In case unknowingly user put a start date that is greater than all obersvation records in it. Ensure to handle this and return empty values
    # Instead of returning an internal server error 
    if (math.isnan(min_temp)):
        tempsummary_results['Temp_Min'] = float(0)
    else:
        tempsummary_results['Temp_Min'] = float(min_temp)

    if (math.isnan(max_temp)):
        tempsummary_results['Temp_Max'] = float(0)
    else:
        tempsummary_results['Temp_Max'] = float(max_temp)

    if (math.isnan(avg_temp)):
        tempsummary_results['Temp_Average'] = float(0)
    else:
        tempsummary_results['Temp_Average'] = float(avg_temp)

    for key in tempsummary_results.keys():
        val = tempsummary_results[key]
        print("Key: ", str(key), 'points to: ', str(val))

    return jsonify(tempsummary_results)

@app.route("/api/v1.0/<start_date>/<end_date>")
def calc_temp_stats_between_startdate_enddate(start_date, end_date):
    # Calculate Minimum, Maximum and Average temperature for all observations taken between start date and end date
    print(start_date)
    print(end_date)
    #print (Measurement)
    #Now Run querue to find the Values to plot min max and average temps 
    results = session.query(Measurement.tobs).\
                filter(and_(Measurement.date <= end_date, Measurement.date >= start_date)).\
                order_by(Measurement.date.desc()).all()
    
    temp_df = pd.DataFrame(results, columns=['tobs'])
    #temp_df.set_index('date', inplace=True, )
    #print ("Return Dataframe is:")
    #print (temp_df)
    #temp_df.head(10)
    
    min_temp = temp_df['tobs'].min()
    print(min_temp)
    
    max_temp = temp_df['tobs'].max()
    print(max_temp)
    
    avg_temp = temp_df['tobs'].mean()
    print(avg_temp)

    tempsummary_results = {}
    tempsummary_results['Start_Date'] = str(start_date)
    tempsummary_results['End_Date'] = str(end_date)
    
    # In case unknowingly user put a start date that is greater than all obersvation records in it. Ensure to handle this and return empty values
    # Instead of returning an internal server error 
    if (math.isnan(min_temp)):
        tempsummary_results['Temp_Min'] = float(0)
    else:
        tempsummary_results['Temp_Min'] = float(min_temp)

    if (math.isnan(max_temp)):
        tempsummary_results['Temp_Max'] = float(0)
    else:
        tempsummary_results['Temp_Max'] = float(max_temp)

    if (math.isnan(avg_temp)):
        tempsummary_results['Temp_Average'] = float(0)
    else:
        tempsummary_results['Temp_Average'] = float(avg_temp)

    for key in tempsummary_results.keys():
        val = tempsummary_results[key]
        print("Key: ", str(key), 'points to: ', str(val))

    return jsonify(tempsummary_results)


if __name__ == '__main__':
    app.run()