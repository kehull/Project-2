DROP TABLE IF EXISTS WILDFIRES;

CREATE TABLE IF NOT EXISTS WILDFIRES (
	incident_name VARCHAR,
	county VARCHAR,
	acres_burned NUMERIC,
	longitude NUMERIC,
	latitude NUMERIC,
	incident_type VARCHAR,
	date_extinguished VARCHAR,
	date_created VARCHAR,
	PRIMARY KEY(incident_name, date_created)
);

COPY WILDFIRES(incident_name, county, acres_burned, longitude, latitude, incident_type, date_extinguished, date_created)
FROM 'C:\Users\kelly\Documents\Completed_Homework\Project-2\data\clean_fire.csv'
DELIMITER ','
CSV HEADER;

DROP TABLE IF EXISTS EARTHQUAKES; 

CREATE TABLE IF NOT EXISTS EARTHQUAKES (
	place VARCHAR,
	time NUMERIC,
	magnitude NUMERIC,
	latitude NUMERIC,
	longitude NUMERIC,
	depth NUMERIC,
	PRIMARY KEY(place, time)
);

COPY EARTHQUAKES(place, time, magnitude, latitude, longitude, depth)
FROM 'C:\Users\kelly\Documents\Completed_Homework\Project-2\data\California_EarthQuake.csv'
DELIMITER ','
CSV HEADER;

DROP TABLE IF EXISTS COUNTIES;

CREATE TABLE IF NOT EXISTS COUNTIES (
	county VARCHAR,
	city VARCHAR,
	polygon VARCHAR,
	PRIMARY KEY(county,city)
);

COPY COUNTIES(county, city, polygon)
FROM 'C:\Users\kelly\Documents\Completed_Homework\Project-2\data\County_Boundaries.csv'
DELIMITER ','
CSV HEADER;