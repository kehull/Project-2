CREATE TABLE IF NOT EXISTS WILDFIRES (
	id NUMERIC UNIQUE NOT NULL,
	incident_name VARCHAR,
	county VARCHAR,
	acres_burned NUMERIC,
	longitude NUMERIC,
	latitude NUMERIC,
	incident_type VARCHAR,
	date_extinguished VARCHAR,
	date_created VARCHAR,
	PRIMARY KEY(id)
);

COPY WILDFIRES(incident_name, county, acres_burned, longitude, latitude, incident_type, date_extinguished, date_created)
FROM 'clean_fire.csv'
DELIMITER ','
CSV HEADER;

CREATE TABLE IF NOT EXISTS EARTHQUAKES (
	id NUMERIC UNIQUE NOT NULL,
	place VARCHAR,
	time NUMERIC,
	magnitude NUMERIC,
	latitude NUMERIC,
	depth NUMERIC,
	PRIMARY KEY(id)
);

COPY EARTHQUAKES(place, time, magnitude, latitude, depth)
FROM 'California_EarthQuake.csv'
DELIMITER ','
CSV HEADER;

CREATE TABLE IF NOT EXISTS COUNTIES (
	id NUMERIC UNIQUE NOT NULL,
	county VARCHAR,
	city VARCHAR,
	polygon VARCHAR,
	PRIMARY KEY(id)
);

COPY COUNTIES(county, city, polygon)
FROM 'County_Boundaries.csv'
DELIMITER ','
CSV HEADER;