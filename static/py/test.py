import numpy as np
import datetime as dt
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

import geoalchemy2

path="../../data/californiadisasters.sqlite"
engine=create_engine(f"sqlite:///{path}")

earthquake_list = []
earthquake_query = engine.execute("SELECT coordinate FROM VW_EARTHQUAKE")

for q in earthquake_query:
    earthquake_list.append(q[0])


counties_list = []
counties_poly = []
counties_query = engine.execute("SELECT DISTINCT county, polygon FROM COUNTIES")

for county, poly in counties_query:
    counties_list.append(county)
    counties_poly.append(poly)

earthquake_county = {}

for i in range(len(earthquake_list)):
    for j in range(len(counties_list)):
        if (geoalchemy2.functions.ST_Intersects(earthquake_list[i], counties_poly[j]) == 1):
            earthquake_county[earthquake_list[i]] = counties_list[j]

print(earthquake_county)