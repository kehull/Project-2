# Dependencies
import requests
import json

# Target data
startdate = "2013-01-01"
enddate = "2021-03-12"
minmagnitude = "5"
minlatitude = "32.30"
minlongitude = "-114.8"
maxlatitude = "42"
maxlongitude = "-124.24"

# Build the endpoint URL
target_url = ('https://earthquake.usgs.gov/fdsnws/event/1/query?format=geojson&starttime={0}&endtime={1}&minmagnitude={2}&minlatitude={3}&minlongitude={4}&maxlatitude={5}&maxlongitude={6}').format(startdate, enddate, minmagnitude, minlatitude, minlongitude, maxlatitude, maxlongitude)
# target_url = ('https://earthquake.usgs.gov/fdsnws/event/1/query?format=geojson&starttime={0}&endtime={1}&minmagnitude={2}').format(startdate, enddate, minmagnitude)

# Request the data
geo_data = requests.get(target_url).json()

# Print the json
print(json.dumps(geo_data, indent=4, sort_keys=True))