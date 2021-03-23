#import dependencies
import os
import sqlalchemy
from sqlalchemy import create_engine, func

from flask import Flask, jsonify, request, render_template, redirect

#database setup
path="data/californiadisasters.sqlite"
engine=create_engine(f"sqlite:///{path}")

#create dates list for checking on for fire api's
dates_list=[]
dates=engine.execute("SELECT date_created FROM WILDFIRES")
for date in dates:
    dates_list.append(date[0])

#create counties list for checking on for fire api's
county_list=[]
counties=engine.execute("SELECT county FROM WILDFIRES")
for county in counties:
    county_list.append(county[0])

#create depth list to check max for earthquake api
depth_list=[]
depth=engine.execute("SELECT depth FROM EARTHQUAKES")
for km in depth:
    depth_list.append(float(km[0]))

#create flask app
app=Flask(__name__)
#ignore key sort
app.config['JSON_SORT_KEYS'] = False


# set 'Home' route 
@app.route("/")
#create function that tells the server when user has entered home page
def welcome():
    print("Server has recieved request for 'Welcome' page...")
    
        # Available routes fire 
        # /api/v1.0/fire  returns entire dataset for fire db
        # /api/v1.0/fire/county/<county>  returns specific county
        # /api/v1.0/fire/date/<date>  returns fires that started on date given
        # /api/v1.0/fire/classification/<classification>  returns fires based on class

        # Available routes earthquake
        # /api/v1.0/earthquake  returns entire dataset for earthquake db
        # /api/v1.0/earthquake/magnitude/<magnitude>  returns earthquakes that are >= magnitude given
        # /api/v1.0/earthquake/depth/<depth> returns  earthquakes that are >= given depth
        # /api/v1.0/earthquake/classification/magnitude/classification/<classification>  returns earthquakes based on magnitude class
        #/api/v1.0/earthquake/classification/depth/classification/<classification>  returns earthquakes based on depth class
    
    # return f"error! Please input proper api path",404
    return render_template("index.html")


#set fire db route
@app.route("/api/v1.0/fire")

# create function that returns fire db results for query
def entire_db():
    
    #create results list to store results from sqlalchemy
    results_list=[]
    #create query
    results=engine.execute("SELECT * FROM WILDFIRES;")
    #loop through query and append to results list
    for result in results:
        results_list.append(result)
    
    #create dictionary to hold data for api
    json_dict={"data":[]}

    #loop through results list
    for name,county,acres_burned,lng,lat,kind,date_extinguished,date_created in results_list:
        #create test_dict to store info for each loop
        test_dict={"properties":{}}
        #populate test_dict
        test_dict["properties"]["name"]=name
        test_dict["properties"]["county"]=county
        test_dict["properties"]["acres_burned"]=acres_burned
        test_dict["properties"]["type"]=kind
        test_dict["properties"]["date_cre"]=date_created
        test_dict["properties"]["date_ext"]=date_extinguished
        test_dict["properties"]["lat"]=lat
        test_dict["properties"]["lng"]=lng
        #add each instance of test_dict to json_dict
        json_dict["data"].append(test_dict)
        
    #return jsonified dictionary
    return jsonify(json_dict)

#repeat mostly for county
@app.route("/api/v1.0/fire/county/<county>")
def location(county):
    #create a string version of argument
    test=f'{county}'
    #create var that changes inpuit to title
    canonicalization=test.title()
    
    if canonicalization in county_list:
        results_list=[]
        results=engine.execute(f"SELECT * FROM WILDFIRES WHERE county LIKE'{canonicalization}%'")
        
        for result in results:
            results_list.append(result)
        
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
        f"error! {county} county not found",404

#repeat for date
@app.route("/api/v1.0/fire/date/<date>")
def one_date(date):
    canonicalization=f'{date}'
    
    if date in dates_list:
        results_list=[]
        results=engine.execute(f"SELECT * FROM WILDFIRES WHERE date_created == '{canonicalization}'")
        
        for result in results:
            results_list.append(result)
        
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

        #return json_dict
        return jsonify(json_dict)
    else: 
        f"error! {date} date not found",404

#repeat for fire classification
@app.route("/api/v1.0/fire/classification/<classification>")
def fire_class(classification):
    test=f'{classification}'
    canonicalization=test.title()
    results_list=[]
    #create blank results that change value depending on conditional
    results=""
    #conditional
    if canonicalization == "G":
        results=engine.execute("SELECT * FROM WILDFIRES WHERE acres_burned >= 5000 ORDER BY acres_burned")
    elif canonicalization =="F":
        results=engine.execute("SELECT * FROM WILDFIRES WHERE acres_burned >= 1000 AND acres_burned <5000 ORDER BY acres_burned")
    elif canonicalization =="E":
        results=engine.execute("SELECT * FROM WILDFIRES WHERE acres_burned >= 300 AND acres_burned <1000 ORDER BY acres_burned")
    elif canonicalization =="D":
        results=engine.execute("SELECT * FROM WILDFIRES WHERE acres_burned >= 100 AND acres_burned <300 ORDER BY acres_burned")
    elif canonicalization =="C":
        results=engine.execute("SELECT * FROM WILDFIRES WHERE acres_burned >= 10 AND acres_burned <100 ORDER BY acres_burned")
    elif canonicalization =="B":
        results=engine.execute("SELECT * FROM WILDFIRES WHERE acres_burned > .25 AND acres_burned <10 ORDER BY acres_burned")
    elif canonicalization =="A":
        results=engine.execute("SELECT * FROM WILDFIRES WHERE acres_burned <=.25 ORDER BY acres_burned")
    else:
        return f"error! {canonicalization} classification not found."
    
    for result in results:
            results_list.append(result)
        
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



#repeat for earthquake db
@app.route("/api/v1.0/earthquake")
def earthquake_db():
    results_list=[]
    results=engine.execute("SELECT * FROM EARTHQUAKES")
    
    for result in results:
        results_list.append(result)
    
    json_dict={"data":[]}
    
    for place, time, mag, lng,lat,depth in results_list:
        test_dict={"properties":{}}
        
        test_dict["properties"]["location"]=place
        test_dict["properties"]["epoch_time"]=time
        test_dict["properties"]["magnitude"]=mag
        test_dict["properties"]["latitude"]=lat
        test_dict["properties"]["longitude"]=lng
        test_dict["properties"]["depth(km)"]=depth
        
        json_dict["data"].append(test_dict)

    return jsonify(json_dict)

#repeat for earthquake magnitude
@app.route("/api/v1.0/earthquake/magnitude/<magnitude>")
def magnitude_return(magnitude):
    canonicalization= int(magnitude)
    if canonicalization <=10:
        results_list=[]
        results=engine.execute(f"SELECT * FROM EARTHQUAKES WHERE magnitude >={canonicalization} ORDER BY magnitude")
        
        for result in results:
            results_list.append(result)

        json_dict={"data":[]}
        
        for place, time, mag, lng,lat,depth in results_list:
            test_dict={"properties":{}}
            
            test_dict["properties"]["location"]=place
            test_dict["properties"]["epoch_time"]=time
            test_dict["properties"]["magnitude"]=mag
            test_dict["properties"]["latitude"]=lat
            test_dict["properties"]["longitude"]=lng
            test_dict["properties"]["depth(km)"]=depth
            
            json_dict["data"].append(test_dict)
        
        return jsonify(json_dict)
    else:
        return f"error! {magnitude} magnitude not found."
#repeat for depth
@app.route("/api/v1.0/earthquake/depth/<depth>") 
def depth_return(depth):
    canonicalization=int(depth)
    if canonicalization <= max(depth_list):
        results_list=[]
        results=engine.execute(f"SELECT * FROM EARTHQUAKES WHERE depth >= {canonicalization} ORDER BY depth")
        
        for result in results:
            results_list.append(result)

        json_dict={"data":[]}
        
        for place, time, mag, lng,lat,depth in results_list:
            test_dict={"properties":{}}
            
            test_dict["properties"]["location"]=place
            test_dict["properties"]["epoch_time"]=time
            test_dict["properties"]["magnitude"]=mag
            test_dict["properties"]["latitude"]=lat
            test_dict["properties"]["longitude"]=lng
            test_dict["properties"]["depth(km)"]=depth
            
            json_dict["data"].append(test_dict)
        
        return jsonify(json_dict)
    else:
        return f"error! {depth} depth not found."

#repeat for magnitude classification
@app.route("/api/v1.0/earthquake/classification/magnitude/classification/<classification>")
def mag_class(classification):
    test=f'{classification}'
    canonicalization=test.title()
    results_list=[]
    results=""
    
    if canonicalization == "Great":
        results=engine.execute("SELECT * FROM EARTHQUAKES WHERE magnitude >=8 ORDER BY magnitude")
    elif canonicalization =="Major":
        results=engine.execute("SELECT * FROM EARTHQUAKES WHERE magnitude >=7 AND magnitude < 8 ORDER BY magnitude")
    elif canonicalization =="Strong":
        results=engine.execute("SELECT * FROM EARTHQUAKES WHERE magnitude >=6 AND magnitude < 7 ORDER BY magnitude")
    elif canonicalization =="Moderate":
        results=engine.execute("SELECT * FROM EARTHQUAKES WHERE magnitude < 6 ORDER BY magnitude")
    else:
        return f"error! {canonicalization} classification not found."
    
    for result in results:
            results_list.append(result)

    json_dict={"data":[]}
    
    for place, time, mag, lng,lat,depth in results_list:
        
        test_dict={"properties":{}}
        test_dict["properties"]["location"]=place
        test_dict["properties"]["epoch_time"]=time
        test_dict["properties"]["magnitude"]=mag
        test_dict["properties"]["latitude"]=lat
        test_dict["properties"]["longitude"]=lng
        test_dict["properties"]["depth(km)"]=depth
        
        json_dict["data"].append(test_dict)
        
    return jsonify(json_dict)

#repeat for depth classification 
@app.route("/api/v1.0/earthquake/classification/depth/classification/<classification>")
def depth_class(classification):
    test=f"{classification}"
    canonicalization=test.title()
    results_list=[]
    results=""
    
    if canonicalization == "Deep":
        results=engine.execute("SELECT * FROM EARTHQUAKES WHERE depth >= 33 ORDER BY depth")
    elif canonicalization =="Mid":
        results=engine.execute("SELECT * FROM EARTHQUAKES WHERE depth >= 17 AND depth <33 ORDER BY depth")
    elif canonicalization =="Shallow":
        results=engine.execute("SELECT * FROM EARTHQUAKES WHERE depth < 17 ORDER BY depth")
    else:
        return f"error! {canonicalization} classification not found."
    
    for result in results:
            results_list.append(result)
    
    json_dict={"data":[]}
    
    for place, time, mag, lng,lat,depth in results_list:
        
        test_dict={"properties":{}}
        test_dict["properties"]["location"]=place
        test_dict["properties"]["epoch_time"]=time
        test_dict["properties"]["magnitude"]=mag
        test_dict["properties"]["latitude"]=lat
        test_dict["properties"]["longitude"]=lng
        test_dict["properties"]["depth(km)"]=depth
        
        json_dict["data"].append(test_dict)
        
    return jsonify(json_dict)
    
#close out flask
if __name__=='__main__':
<<<<<<< HEAD
    app.run(debug=True)
=======
    app.run(debug=True)
>>>>>>> main
