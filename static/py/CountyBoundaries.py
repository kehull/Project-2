# Dependencies
import requests
import json
import pandas as pd
# import datetime as dt

target_url = ('https://opendata.arcgis.com/datasets/35487e8c86644229bffdb5b0a4164d85_0.geojson')

# Request the data
geo_data = requests.get(target_url).json()

# build columns of dataframe
county = []
city = []
polygon = []


# populate columns
for response in geo_data['features']:
    county.append(response['properties']['COUNTY'])
    city.append(response['properties']['CITY'])
    polygon.append(response['geometry']['coordinates'])


# build dataframe
boundaries_df = pd.DataFrame({
    "county": county,
    "city": city,
    "polygon": polygon
})

boundaries_df.drop_duplicates()

# print(boundaries_df)

boundaries_df.to_csv('data/County_Boundaries.csv', index=False)