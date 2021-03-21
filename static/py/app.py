#import dependencies
import numpy as np
import datetime as dt
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

#database setup
path="../../data/wildfires.sqlite"
engine=create_engine(f"sqlite:///{path}")
Base = automap_base()
Base.prepare(engine,reflect=True)
results_test=engine.execute("SELECT * FROM WILDFIRES")




# results_test_list_2=[]
# results_test_2=engine.execute("SELECT * FROM WILDFIRES WHERE date_created >= '12/4/2017'")
# for result in results_test_2:
#     results_test_list_2.append(result)
# print(results_test_list_2)


# earthquake=Base.classes.earthquake
dates_list=[]
dates=engine.execute("SELECT date_created FROM WILDFIRES")
for date in dates:
    dates_list.append(date[0])

# print(dates_list)

 
county_list=[]
counties=engine.execute("SELECT county FROM WILDFIRES")
for county in counties:
    county_list.append(county[0])


app=Flask(__name__)
app.config['JSON_SORT_KEYS'] = False

# set 'Home' route 
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
    
    
    
    #filter query by station with most measurments
    results_list=[]
    results=engine.execute("SELECT * FROM WILDFIRES;")
    for result in results:
        results_list.append(result)
    
    
    
     #close session for efficiency   
    
    
    
    #create dictionary that uses date as key and precipitation as value
    json_dict={"data":[]}

    
   
    
    
    for name,county,acres_burned,lng,lat,kind,date_extinguished,date_created in results_list:

        test_dict={"properties":{}}
    
        test_dict["properties"]["name"]=name
        test_dict["properties"]["county"]=county
        test_dict["properties"]["acres_burned"]=acres_burned
        test_dict["properties"]["type"]=kind
        test_dict["properties"]["date_cre"]=date_created
        test_dict["properties"]["date_ext"]=date_extinguished
        test_dict["properties"]["lat"]=lat
        test_dict["properties"]["lng"]=lng
        json_dict["data"].append(test_dict)
        



        
        
        
    #     #return jsonified dictionary
    return jsonify(json_dict)

@app.route("/api/v1.0/fire/<county>")
def location(county):
    canonicalization=f'{county}'
    
    if county in county_list:
        results_list=[]
        results=engine.execute(f"SELECT * FROM WILDFIRES WHERE county LIKE'{canonicalization}%'")
        
        for result in results:
            results_list.append(result)
        print(results_list)
        json_dict={"data":[]}
     
    
        for name,county,acres_burned,lng,lat,kind,date_extinguished,date_created in results_list:

            test_dict={"properties":{}}
    
            test_dict["properties"]["name"]=name
            test_dict["properties"]["county"]=county
            test_dict["properties"]["acres_burned"]=acres_burned
            test_dict["properties"]["type"]=kind
            test_dict["properties"]["date_cre"]=date_created
            test_dict["properties"]["date_ext"]=date_extinguished
            test_dict["properties"]["lat"]=lat
            test_dict["properties"]["lng"]=lng
            json_dict["data"].append(test_dict)



        
        
        
        #return jsonified dictionary
        return jsonify(json_dict)
    else: 
        f"error! {county} not found",404

#set route for start date only
@app.route("/api/v1.0/fire/date/<start>")
def one_date(start):
    canonicalization=f'{start}'
    
    
    if start in dates_list:
        results_list=[]
        results=engine.execute(f"SELECT * FROM WILDFIRES WHERE date_created >= '{canonicalization}'")
        
        for result in results:
            results_list.append(result)
        print(results_list)
        json_dict={"data":[]}
     
    
        for name,county,acres_burned,lng,lat,kind,date_extinguished,date_created in results_list:

            test_dict={"properties":{}}
    
            test_dict["properties"]["name"]=name
            test_dict["properties"]["county"]=county
            test_dict["properties"]["acres_burned"]=acres_burned
            test_dict["properties"]["type"]=kind
            test_dict["properties"]["date_cre"]=date_created
            test_dict["properties"]["date_ext"]=date_extinguished
            test_dict["properties"]["lat"]=lat
            test_dict["properties"]["lng"]=lng
            json_dict["data"].append(test_dict)



        
        
        
        #return jsonified dictionary
        return jsonify(json_dict)
    else: 
        f"error! {start} not found",404



# #repeat procoss of start date to date range
# @app.route("/api/v1.0/fire/date<start>/<end>")
# def date_range(start=None,end=None):
    
#     if start in dates_list and end in dates_list and end > start:
#         session=Session(engine)
#         results_2=session.query(fire).\
#         filter(fire.incident_dateonly_created >= start).\
#         filter(fire.incident_dateonly_extinguished<= end).all()
    
#         session.close()
#         json_list=[]
     
    
#         for name, ongoing, update, date,unit,unit_url,county,location,acres,containment, control, agency,lng, lat, kind,id,url,extinguished, date_ext,dat_cre,active,cal_inc,noti in results_2:
#             features_dict={}
#             coordinates_dict={}   
#             features_dict["name"]=name
#             features_dict["ongoing"]=ongoing
#             features_dict["last_update"]=update
#             features_dict["date_created"]=date
#             features_dict["unit"]=unit
#             features_dict["unit_url"]=unit_url
#             features_dict["county"]=county
#             features_dict["location"]=location
#             features_dict["acres_burned"]=acres
#             features_dict["containment"]=containment
#             features_dict["incident_control"]=control
#             features_dict["agency"]=agency
#             features_dict["type"]=kind
#             features_dict["id"]=id
#             features_dict["url"]=url
#             features_dict["ext_datetime"]=extinguished
#             features_dict["ext_date"]=date_ext
#             features_dict["date_created"]=dat_cre
#             features_dict["active"]=active
#             features_dict["calfire"]=cal_inc
#             features_dict["notification_desired"]=noti
#             coordinates_dict["lat"]=lat
#             coordinates_dict["lng"]=lng     

#             json_list.append(features_dict)
#             json_list.append(coordinates_dict)



        
        
        
#         #return jsonified dictionary
#         return jsonify(json_list)
#     else: 
#         f"error! Range {start} : {end} not found",404


#close out flask
if __name__=='__main__':
    app.run(debug=True)