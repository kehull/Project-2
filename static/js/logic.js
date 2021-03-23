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

// Format Date from epoch to mm-dd-yyyy
function friendlyDate(date) {
  var d = new Date(date),
      month = '' + (d.getMonth() + 1),
      day = '' + d.getDate(),
      year = d.getFullYear();

  if (month.length < 2) 
      month = '0' + month;
  if (day.length < 2) 
      day = '0' + day;

  return [month, day, year].join('-');
}

// Format Date for comparisons
function formatDate(date) {
  var newdate = new Date(date);
  return newdate
}

// find the button (id in HTML is filter-btn)
var button = d3.select("#filter");

// find the form (id in HTML is form-group)
var form = d3.select("#form-group");

var fireData = []
d3.json("http://127.0.0.1:5000/api/v1.0/fire", function(response) {
  for (var i =0; i < response["data"].length; i++) {
    fireData.push(response["data"][i]["properties"])
  }
});

var earthquakeData = []
d3.json("http://127.0.0.1:5000/api/v1.0/earthquake", function(response) {
  for (var i =0; i < response["data"].length; i++) {
    earthquakeData.push(response["data"][i]["properties"])
  }
});

// set filtered data to default values
var filteredFire = fireData // add default values
var filteredEarthquake = earthquakeData // add default values

// create filter function for datasets
function filterData() {

  // Prevent the page from refreshing
  d3.event.preventDefault();

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

  if (inputValue_start !== null || inputValue_start !== '') {
    // filteredFire = filteredFire.filter(data => console.log(data.date_cre));// >= inputValue_start);
    console.log("There is a start date.")
    console.log("the start date is:" + inputValue_start)
     // The 0 there is the key, which sets the date to the epoch
    filteredEarthquake = filteredEarthquake.filter(function(data){
      var d = formatDate(data["epoch_time"]);

      if (d >= formatDate(inputValue_start)){
        console.log(d)
      };
      
    }); // >= inputValue_start);
  }
  else {
    // filteredFire = filteredFire.filter(data => Date.parse(data.date_cre) >= Date.parse('01/01/2013'));
    console.log("There is not a start date.")
    // filteredEarthquake = filteredEarthquake.filter(data => d.setUTCSeconds(data["epoch_time"]) >= '01/01/2013');
  };

  if (inputValue_end !== null || inputValue_end !== '') {
    // filteredFire = filteredFire.filter(data => Date.parse(data.date_cre) < inputValue_end);
    console.log("There is an end date.")
    // filteredEarthquake = filteredEarthquake.filter(data => d.setUTCSeconds(data["epoch_time"]) <= inputValue_end);
  }
  else {
    // filteredFire = filteredFire.filter(data => Date.parse(data.date_cre) < Date.parse(getToday()));
    console.log("There is not an end date.")
    // filteredEarthquake = filteredEarthquake.filter(data => d.setUTCSeconds(data["epoch_time"]) <= getToday());
  };

  // if (inputValue_fire == null || inputValue_fire == '') {
  //   filteredFire = {}
  // };

  // if (inputValue_earthquake == null || inputValue_earthquake == '') {
  //   filteredEarthquake = {}
  // };

  updateVisualizations(filteredFire, filteredEarthquake)
};

// DANGER POINTS FUNCTION _______________________________________________________________________
function dangerScores(filtered_Fire, filtered_Earthquake){

};

// CREATE FIRE MAP ______________________________________________________________________________
function fireMap(fire_Data) {
  var heatArray=[];
  
  for (var i=0; i< fire_Data.length; i++){
    var lat = fire_Data[i]["lat"]
    var lng = fire_Data[i]["lng"]
    heatArray.push([lng,lat])
  }
  var heat= L.heatLayer(heatArray,{
    radius: 20,
    blur:35
  }).addTo(myMap);

};

// CREATE EARTHQUAKE MAP ________________________________________________________________________
function earthquakeMap(earthquake_Data) {
  
};

// CREATE BAR CHART _____________________________________________________________________________
function plotBarChart(filtered_Fire, filtered_Earthquake) {
  // get data
  [counties, points] = dangerScores(filtered_Fire, filtered_Earthquake)

  var trace1 = {
    x: counties,
    y: points,
    type: "bar"
  };

  var data = [trace1];

  var layout = {
    title: "'Bar' Chart"
  };

  Plotly.newPlot("chartid", data, layout);
};


// FUNCTION TO UPDATE VISUALIZATIONS ______________________________________________________________
function updateVisualizations(filtered_Fire, filtered_Earthquake) {
  // [filtered_Fire, filtered_Earthquake] = filterData()
  
  console.log(filtered_Fire)
  console.log(filtered_Earthquake)
  
  // Update Fire Map
  // fireMap(fire_Data)

  // Update Earthquake Map
  // earthquakeMap(earthquake_Data)

  // Update Bar Chart
  // plotBarChart()
};

// CALL THE FUNCTIONS _____________________________________________________________________________
  fireMap(filteredFire)
  // earthquakeMap(filteredEarthquake)
  // plotBarChart(filteredFire, filteredEarthquake)

// D3 Listener ____________________________________________________________________________________
button.on("click", filterData);
form.on("submit",filterData);