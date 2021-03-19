#import dependencies
import numpy as np
import datetime as dt
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

#database setup
path=""
engine=create_engine(f"sqlite:///{path}")
Base = automap_base()
Base.prepare(engine,reflect=True)

earthquake=Base.classes.earthquake
fire= Base.classes.fire

dates_list=[]
county_list=[]
#may have to unravel query lists

app=Flask(__name__)

#set 'Home' route
@app.route("/")
#create function that displays instructions for the pathways
def welcome():
    print("Server has recieved request for 'Welcome' page...")
    
        # Available routes fire test
        # f"/api/v1.0/fire"  returns entire dataset for 
        # f"/api/v1.0/fire/COUNTY<br/>" returns specific county
        # f"/api/v1.0/fire/incident/BOOLEAN" returns fires that are over or still going
        # f"/api/v1.0/fire/date/START<br/>" returns fires that started on and after date given
        # f"/api/v1.0/fire/date/START/END" returns  date range entered
    

#set precipitation route
@app.route("/api/v1.0/fire")
# create function that returns precipitation results for query
def entire_db():
    session=Session(engine)
    
    
    #filter query by station with most measurments
    results=session.query(fire).all()
    
     #close session for efficiency   
    session.close()
    
    
    #create dictionary that uses date as key and precipitation as value
    json_list=[]
     
    
    for name, ongoing, update, date,unit,unit_url,county,location,acres,containment, control, agency,lng, lat, kind,id,url,extinguished, date_ext,dat_cre,active,cal_inc,noti in results:
        features_dict={}
        coordinates_dict={}   
        features_dict["name"]=name
        features_dict["ongoing"]=ongoing
        features_dict["last_update"]=update
        features_dict["date_created"]=date
        features_dict["unit"]=unit
        features_dict["unit_url"]=unit_url
        features_dict["county"]=county
        features_dict["location"]=location
        features_dict["acres_burned"]=acres
        features_dict["containment"]=containment
        features_dict["incident_control"]=control
        features_dict["agency"]=agency
        features_dict["type"]=kind
        features_dict["id"]=id
        features_dict["url"]=url
        features_dict["ext_datetime"]=extinguished
        features_dict["ext_date"]=date_ext
        features_dict["date_created"]=dat_cre
        features_dict["active"]=active
        features_dict["calfire"]=cal_inc
        features_dict["notification_desired"]=noti
        coordinates_dict["lat"]=lat
        coordinates_dict["lng"]=lng     

        json_list.append(features_dict)
        json_list.append(coordinates_dict)



        
        
        
        #return jsonified dictionary
    return jsonify(json_list)

@app.route("/api/v1.0/fire/<county>")
def county(County):
    canonicalization=f'{county}'
    if County in county_list:
        session=Session(engine)
        results=session.query(fire).filter(fire.incident_county == canonicalization).\
            order_by(fire.incident_county).all()
        session.close()

        json_list=[]
     
    
        for name, ongoing, update, date,unit,unit_url,county,location,acres,containment, control, agency,lng, lat, kind,id,url,extinguished, date_ext,dat_cre,active,cal_inc,noti in results:
            features_dict={}
            coordinates_dict={}   
            features_dict["name"]=name
            features_dict["ongoing"]=ongoing
            features_dict["last_update"]=update
            features_dict["date_created"]=date
            features_dict["unit"]=unit
            features_dict["unit_url"]=unit_url
            features_dict["county"]=county
            features_dict["location"]=location
            features_dict["acres_burned"]=acres
            features_dict["containment"]=containment
            features_dict["incident_control"]=control
            features_dict["agency"]=agency
            features_dict["type"]=kind
            features_dict["id"]=id
            features_dict["url"]=url
            features_dict["ext_datetime"]=extinguished
            features_dict["ext_date"]=date_ext
            features_dict["date_created"]=dat_cre
            features_dict["active"]=active
            features_dict["calfire"]=cal_inc
            features_dict["notification_desired"]=noti
            coordinates_dict["lat"]=lat
            coordinates_dict["lng"]=lng     

            json_list.append(features_dict)
            json_list.append(coordinates_dict)



        
        
        
        #return jsonified dictionary
        return jsonify(json_list)
    else: 
        f"error! {boolean} not found",404
# set route for tobs
@app.route("/api/v1.0/fire/incident/<boolean>")
#same repeated process as the precipatition route
def boolean(Boolean):
    canonicalization=f'{boolean}'
    
    session=Session(engine)
    results = session.query(fire).filter(fire.incident_is_final== canonicalization).\
        order_by(fire.incident_county).all()
    session.close()
    json_list=[]
     
    
    for name, ongoing, update, date,unit,unit_url,county,location,acres,containment, control, agency,lng, lat, kind,id,url,extinguished, date_ext,dat_cre,active,cal_inc,noti in results:
        features_dict={}
        coordinates_dict={}   
        features_dict["name"]=name
        features_dict["ongoing"]=ongoing
        features_dict["last_update"]=update
        features_dict["date_created"]=date
        features_dict["unit"]=unit
        features_dict["unit_url"]=unit_url
        features_dict["county"]=county
        features_dict["location"]=location
        features_dict["acres_burned"]=acres
        features_dict["containment"]=containment
        features_dict["incident_control"]=control
        features_dict["agency"]=agency
        features_dict["type"]=kind
        features_dict["id"]=id
        features_dict["url"]=url
        features_dict["ext_datetime"]=extinguished
        features_dict["ext_date"]=date_ext
        features_dict["date_created"]=dat_cre
        features_dict["active"]=active
        features_dict["calfire"]=cal_inc
        features_dict["notification_desired"]=noti
        coordinates_dict["lat"]=lat
        coordinates_dict["lng"]=lng     

        json_list.append(features_dict)
        json_list.append(coordinates_dict)



        
        
        
        #return jsonified dictionary
    return jsonify(json_list)
    

#set route for start date only
@app.route("/api/v1.0/fire/date/<start>")
def one_date(start):
    #created variable to store the string of start
    canonicalization=f'{start}'
    
    #check to see if date entered in url is valid
    if start in dates_list:
        #create session
        session=Session(engine)
        
        #create query saved to results
        results=session.query(fire).filter(fire.incident_dateonly_created >= canonicalization).\
            order_by(fire.incident_dateonly_created).all()
        session.close()
        
        #create list of dictionaries that will display query
        #testing a few aestetics for data display
        #create blank list
        json_list=[]
     
    
        for name, ongoing, update, date,unit,unit_url,county,location,acres,containment, control, agency,lng, lat, kind,id,url,extinguished, date_ext,dat_cre,active,cal_inc,noti in results:
            features_dict={}
            coordinates_dict={}   
            features_dict["name"]=name
            features_dict["ongoing"]=ongoing
            features_dict["last_update"]=update
            features_dict["date_created"]=date
            features_dict["unit"]=unit
            features_dict["unit_url"]=unit_url
            features_dict["county"]=county
            features_dict["location"]=location
            features_dict["acres_burned"]=acres
            features_dict["containment"]=containment
            features_dict["incident_control"]=control
            features_dict["agency"]=agency
            features_dict["type"]=kind
            features_dict["id"]=id
            features_dict["url"]=url
            features_dict["ext_datetime"]=extinguished
            features_dict["ext_date"]=date_ext
            features_dict["date_created"]=dat_cre
            features_dict["active"]=active
            features_dict["calfire"]=cal_inc
            features_dict["notification_desired"]=noti
            coordinates_dict["lat"]=lat
            coordinates_dict["lng"]=lng     

            json_list.append(features_dict)
            json_list.append(coordinates_dict)



        
        
        
        #return jsonified dictionary
        return jsonify(json_list)
    else: 
        f"error! {start} not found",404



#repeat procoss of start date to date range
@app.route("/api/v1.0/fire/date<start>/<end>")
def date_range(start=None,end=None):
    
    if start in dates_list and end in dates_list and end > start:
        session=Session(engine)
        results_2=session.query(fire).\
        filter(fire.incident_dateonly_created >= start).\
        filter(fire.incident_dateonly_extinguished<= end).all()
    
        session.close()
        json_list=[]
     
    
        for name, ongoing, update, date,unit,unit_url,county,location,acres,containment, control, agency,lng, lat, kind,id,url,extinguished, date_ext,dat_cre,active,cal_inc,noti in results_2:
            features_dict={}
            coordinates_dict={}   
            features_dict["name"]=name
            features_dict["ongoing"]=ongoing
            features_dict["last_update"]=update
            features_dict["date_created"]=date
            features_dict["unit"]=unit
            features_dict["unit_url"]=unit_url
            features_dict["county"]=county
            features_dict["location"]=location
            features_dict["acres_burned"]=acres
            features_dict["containment"]=containment
            features_dict["incident_control"]=control
            features_dict["agency"]=agency
            features_dict["type"]=kind
            features_dict["id"]=id
            features_dict["url"]=url
            features_dict["ext_datetime"]=extinguished
            features_dict["ext_date"]=date_ext
            features_dict["date_created"]=dat_cre
            features_dict["active"]=active
            features_dict["calfire"]=cal_inc
            features_dict["notification_desired"]=noti
            coordinates_dict["lat"]=lat
            coordinates_dict["lng"]=lng     

            json_list.append(features_dict)
            json_list.append(coordinates_dict)



        
        
        
        #return jsonified dictionary
        return jsonify(json_list)
    else: 
        f"error! Range {start} : {end} not found",404


#close out flask
if __name__=='__main__':
    app.run(debug=True)