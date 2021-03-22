// CREATE COUNTIES MAP ______________________________________________________________________________
// Creating map object
var myMap = L.map("mapid", {
  center: [36.7783, -119.4179],
  zoom: 5
});

// Adding tile layer
L.tileLayer("https://api.mapbox.com/styles/v1/{id}/tiles/{z}/{x}/{y}?access_token={accessToken}", {
  attribution: "© <a href='https://www.mapbox.com/about/maps/'>Mapbox</a> © <a href='http://www.openstreetmap.org/copyright'>OpenStreetMap</a> <strong><a href='https://www.mapbox.com/map-feedback/' target='_blank'>Improve this map</a></strong>",
  tileSize: 512,
  maxZoom: 18,
  zoomOffset: -1,
  id: "mapbox/streets-v11",
  accessToken: API_KEY
}).addTo(myMap);

// Use this link to get the geojson data.
var link = "https://opendata.arcgis.com/datasets/35487e8c86644229bffdb5b0a4164d85_0.geojson";

// Grabbing our GeoJSON data..
d3.json(link, function(data) {
  // Creating a GeoJSON layer with the retrieved data
  L.geoJson(data).addTo(myMap);
});


// FILTER FUNCTIONS ______________________________________________________________________________
// get current date
function getToday() {
  var today = new Date();
  var dd = String(today.getDate()).padStart(2, '0');
  var mm = String(today.getMonth() + 1).padStart(2, '0'); //January is 0!
  var yyyy = today.getFullYear();
  today = mm + '/' + dd + '/' + yyyy;

//   var date = new Date(dateTime.getTime());
//   date.setHours(0, 0, 0, 0);
  return today;
}

// find the button (id in HTML is filter-btn)
var button = d3.select("#filter");

// find the form (id in HTML is form-group)
var form = d3.select("#form-group");

var fireData = d3.json("http://127.0.0.1:5000/api/v1.0/fire", d => d['data'])
var earthquakeData = d3.json("http://127.0.0.1:5000/api/v1.0/earthquake", d => d['data']);

// set filtered data to default values
var filteredFire = fireData // add default values
var filteredEarthquake = earthquakeData // add default values

// create filter function for datasets
function filterData() {
  // Prevent the page from refreshing
  // d3.event.preventDefault();

  var d = new Date(0); // The 0 there is the key, which sets the date to the epoch

  // Select the input element and get the raw HTML node
  var inputElement_startdate = d3.select("#startdate");
  var inputElement_enddate = d3.select("#enddate");
  var inputElement_excludeFire = d3.select("#fireform");
  var inputElement_excludeEarthquake = d3.select("#earthquake");

  // Get the value property of the input element
  var inputValue_start = inputElement_startdate.property("value");
  var inputValue_end = inputElement_enddate.property("value");
  var inputValue_fire = inputElement_excludeFire.property("value");
  var inputValue_earthquake = inputElement_excludeEarthquake.property("value");

  var filteredFire = fireData
  var filteredEarthquake = earthquakeData

  if (inputValue_start !== null && inputValue_start !== '') {
    filteredFire = filteredFire.filter(data => data["properties"]["date_cre"] > inputValue_start);
    filteredEarthquake = filteredEarthquake.filter(data => d.setUTCSeconds(data["properties"]["epoch_time"]) > inputValue_start);
  }
  else {
    filteredFire = filteredFire.filter(data => data["properties"]["date_cre"] > '01/01/2013');
    filteredEarthquake = filteredEarthquake.filter(data => d.setUTCSeconds(data["properties"]["epoch_time"]) > '01/01/2013');
  };

  if (inputValue_end !== null && inputValue_end !== '') {
    filteredFire = filteredFire.filter(data => data["properties"]["date_cre"] < inputValue_end);
    filteredEarthquake = filteredEarthquake.filter(data => d.setUTCSeconds(data["properties"]["epoch_time"]) < inputValue_end);
  }
  else {
    filteredFire = filteredFire.filter(data => data["properties"]["date_cre"] < getToday());
    filteredEarthquake = filteredEarthquake.filter(data => d.setUTCSeconds(data["properties"]["epoch_time"]) < getToday());
  };

  if (inputValue_fire == null && inputValue_fire == '') {
    filteredFire = {}
  };

  if (inputValue_earthquake == null && inputValue_earthquake == '') {
    filteredEarthquake = {}
  };


  return filteredFire, filteredEarthquake
};

// DANGER POINTS FUNCTION _______________________________________________________________________


// CREATE FIRE MAP ______________________________________________________________________________


// CREATE EARTHQUAKE MAP ________________________________________________________________________


// CREATE BAR CHART _____________________________________________________________________________
// function plotBarChart(){
//   // get data
//   [filteredFire, filteredEarthquake] = filteredData()
//   [counties, points] = dangerPoints(filteredFire, filteredEarthquake)

//   var trace1 = {
//     x: counties,
//     y: points,
//     type: "bar"
//   };

//   var data = [trace1];

//   var layout = {
//     title: "'Bar' Chart"
//   };

//   Plotly.newPlot("chartid", data, layout);
// };


// // FUNCTION TO UPDATE VISUALIZATIONS ______________________________________________________________
// function updateVisualizations() {
//   // Update Fire Map
  
//   // Update Earthquake Map

//   // Update Bar Chart
//   plotBarChart()
// };

// // CALL THE FUNCTIONS _____________________________________________________________________________
// button.on("click", updateVisualizations);
// form.on("submit",updateVisualizations);