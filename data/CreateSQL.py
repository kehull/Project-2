# Import required libraries 
import sqlite3 
import pandas as pd 
import spatialite

# Connect to SQLite database 
conn = sqlite3.connect(r'californiadisasters.sqlite') 
  
# Load CSV data into Pandas DataFrame 
fire_db = pd.read_csv('clean_fire.csv') 
# Write the data to a sqlite table 
fire_db.to_sql('WILDFIRES', conn, if_exists='replace', index=False) 
  
# Create a cursor object 
cur = conn.cursor() 

# # Fetch and display result 
# for row in cur.execute('SELECT * FROM WILDFIRES'): 
#     print(row) 

# Load CSV data into Pandas DataFrame 
earthquake_db = pd.read_csv('California_EarthQuake.csv') 
# Write the data to a sqlite table 
earthquake_db.to_sql('EARTHQUAKES', conn, if_exists='replace', index=False) 
  
# # Fetch and display result 
# for row in cur.execute('SELECT * FROM EARTHQUAKES'): 
#     print(row) 

# Load CSV data into Pandas DataFrame 
counties_db = pd.read_csv('County_Boundaries.csv') 
# Write the data to a sqlite table 
counties_db.to_sql('COUNTIES', conn, if_exists='replace', index=False) 
  
# # Fetch and display result 
# for row in cur.execute('SELECT * FROM COUNTIES'): 
#     print(row) 

# Create the view which has a single coordinate for the Earthquake Data
cur.execute('DROP VIEW IF EXISTS VW_EARTHQUAKE')
cur.execute("CREATE VIEW VW_EARTHQUAKE AS SELECT EARTHQUAKES.place, EARTHQUAKES.time, EARTHQUAKES.magnitude, EARTHQUAKES.depth, ('[' + EARTHQUAKES.Latitude + ',' + EARTHQUAKES.Longitude + ']') AS coordinate FROM EARTHQUAKES")

# # Fetch and display result 
# for row in cur.execute('SELECT * FROM VW_EARTHQUAKE'): 
#     print(row) 

# Create the view that does the geospacial join to grab the county each earthquake was
cur.execute('DROP VIEW IF EXISTS VW_SPATIAL_EARTHQUAKE')
cur.execute('CREATE VIEW VW_SPATIAL_EARTHQUAKE AS SELECT VW_EARTHQUAKE.place, COUNTIES.County, VW_EARTHQUAKE.time, VW_EARTHQUAKE.magnitude, VW_EARTHQUAKE.depth, VW_EARTHQUAKE.coordinate FROM COUNTIES INNER JOIN VW_EARTHQUAKE ON COUNTY.polygon.STIntersects(VW_EARTHQUAKE.coordinate) = 1')

# # Fetch and display result 
# for row in cur.execute('SELECT * FROM VW_SPATIAL_EARTHQUAKE'): 
#     print(row) 

# Close connection to SQLite database 
conn.close()