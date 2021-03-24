# California Disasters and Habitability
## Project 2
### Kelly Hull, Ali Emily, Janelle Goddard, David Fournie
### 03/24/21
<br><br>

## Link
https://california-disasters.herokuapp.com/
<br><br>

## Notes on Development and Use

Data:
Data used in this project:

Earthquake data from USGS
Wildfire data from Cal Fire
California county border shapes from the California State Geoportal
Wildfire csv file cleaned by Janelle earthquake csv cleaned by Ali, county data for earthquake locations webscraped in Python by Kelly using City to County Finder by StatsAmerica and Wikipedia.

SQLite database created and populated by Kelly using. API created in Python by David.

Map created in Leaflet. Earthquakes mapped in Javascript by Kelly. SVGs for earthquake markers made by Freepik from www.flaticon.com and colored by Kelly. Fires mapped in Javascript by David, Ali, and Janelle. County shape layer placed on map by Ali in Javascript. Data filtering function created by Ali in Javascript. Bar chart visualization created by Janelle and Ali in Javascript using the Highcharts JS library.

Note regarding the wildfire visualization: while we are confident that the location information used in our analysis of the wildfires is accurate, upon plotting the latitude/longitude data provided by Cal Fire, we noticed that many coordinates fell outside of California's borders, even in the ocean, some as far away as North Carolina, or even off the coast of Spain. We believe the coordinate data was entered inaccurately for a number of wildfires. We are also suspicious that older data may have been entered inconsistently, as there are so few fires for years in the earlier part of the dataset. Given more time, we would have used a web scraper or library to designate coordinates for each county in the dataset and re-plotted according to those coordinates, so that we could at least get a more accurate visualization of recent fires.

Data analysis performed by Kelly in Python. Bar chart visualization created by Janelle and Ali in Javascript.

Web Development
Bootstrap development and Heroku deployment managed by David. HTML/CSS, website text, and Fotorama image carousel managed by Kelly. Javascript managed by Ali.


<br><br>

## API Documentation
Base: https://california-disasters.herokuapp.com/api/v1.0

To connect to the fire and earthquake databases, simply add "fire" or "earthquake" to the end of the api base.

Example Fire: https://california-disasters.herokuapp.com/api/v1.0/fire
Example Earthquake: https://california-disasters.herokuapp.com/api/v1.0/earthquake

In the fire db, the database can also be queried by county. Simplt add "/county" and county name after the fire query.

Example: https://california-disasters.herokuapp.com/api/v1.0/fire/yuba

Furthermore, the fire db can be queried by date by adding "/date" and "mm-dd-yyyy" after fire. Months 1-9 are single character entries.
Example: https://california-disasters.herokuapp.com/api/v1.0/fire/date/8-3-2020

According to the Natinal Wildfire Coordinating Group, wildfires are classified into seven groups based on how many acres burned.

Class A:"One-fourth acre or less"
Class B:"More than one-fourth acre, but less than 10 acres"
Class C:"10 acres or more, but less than 100 acres"
Class D:"100 acres or more, but less than 300 acres"
Class E:"300 acres or more, but less than 1,000 acres"
Class F:"1,000 acres or more, but less than 5,000 acres"
Class G:"5,000 acres or more"

Source: https://www.nwcg.gov/term/glossary/size-class-of-fire

The Fire database has been designed to query based on these six classes. Simply add "/classification" and the classification letter at the end of the fire query.

Example: https://california-disasters.herokuapp.com/api/v1.0/fire/classification/a

The Earthquake database is queried in similar fashions. To query the database on earthquake magnitude, simply add "/magnitude" and the richter-scale value(1-10) of the earthquake to the earthquake query.

Example: https://california-disasters.herokuapp.com/api/v1.0/earthquake/magnitude/5

Depth has also been included as a query option. Simply add "/depth" and the depth km to the end of earthquake query. Note: km values range from 1 to 28.

Example: https://california-disasters.herokuapp.com/api/v1.0/earthquake/depth/15

Earthquakes are classified both on their magnitude and depth. Earthquake magnitudes are divided into four categories:

Moderate: Magnitude less than 6
Strong: Magnitude 6-7(exclusive)
Major: Magnitude 7-8(exclusive)
Great: Magnitude 8 and above

To query the earthquake database on magnitude classification, simply add "/magnitude/classification" and the classification.

Example:https://california-disasters.herokuapp.com/api/v1.0/earthquake/magnitude/classification/great

Likewise, earthquakes are also categorized by depth. Earthquake depths are divided into three categories from deep(minor earthquake) to shallow(major earthquake). The classes are:

Deep: More than 33km deep
Mid: Between 17km and 33km deep
Shallow: Less than 17 km

To query on depth classification simply add "/depth/classification" and the classification to the earthquake query.

Example:https://california-disasters.herokuapp.com/api/v1.0/earthquake/depth/classification/mid

Happy quering! <br><br>

## Files Included
The root of the directory conatins app.py which the application runs from, Procfile which runs the gunicorn for Heroku,Project_2.ipynb, used for cleaning data, the readme, and folders for different aspects of the project. The data folder contains all relevant csv, sqlite, and ipynb files that were used to display and modify data. The headshots contains headshot files used for fotorama. The prepwork contains our website sketch and our project proposal. The preview folder contains a screenshot of the website. The static folder contains all css, js, and py files used in our application and data modification, and the templates folder contains all the html files used for the website.

## Website Preview
![Website Preview](preview/california_disasters_preview.png)

