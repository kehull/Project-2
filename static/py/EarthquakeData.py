# Dependencies
import requests
import json
import pandas as pd
# import datetime as dt

# Target data
startdate = "2013-01-01"
enddate = "2021-03-12"
minmagnitude = "5"
minlatitude = "32.30"
minlongitude = "-114.8"
maxlatitude = "42"
maxlongitude = "-124.24"

# Build the endpoint URL
# target_url = ('https://earthquake.usgs.gov/fdsnws/event/1/query?format=geojson&starttime={0}&endtime={1}&minmagnitude={2}&minlatitude={3}&minlongitude={4}&maxlatitude={5}&maxlongitude={6}').format(startdate, enddate, minmagnitude, minlatitude, minlongitude, maxlatitude, maxlongitude)
target_url = ('https://earthquake.usgs.gov/fdsnws/event/1/query?format=geojson&starttime={0}&endtime={1}&minmagnitude={2}').format(startdate, enddate, minmagnitude)

# Request the data
geo_data = requests.get(target_url).json()

# build columns of dataframe
place = []
time = []
mag = []
lat = []
lon = []
depth = []

strSuffix1 = "California"
strSuffix2 = "CA"

# populate columns
for response in geo_data['features']:
    if (response['properties']['place'].endswith(strSuffix1) | response['properties']['place'].endswith(strSuffix2)):
        place.append(response['properties']['place'])
        mag.append(response['properties']['mag'])
        lat.append(response['geometry']['coordinates'][1])
        lon.append(response['geometry']['coordinates'][0])
        depth.append(response['geometry']['coordinates'][2])

        # utcSeconds = response['properties']['time']
        # timeStamp = dt.datetime.fromtimestamp(utcSeconds).strftime('%c')
        time.append(response['properties']['time'])

# build dataframe
earthquake_df = pd.DataFrame({
    "place": place,
    "time": time,
    "magnitude": mag,
    "latitude": lat,
    "longitude": lon,
    "depth": depth
})

print(earthquake_df)