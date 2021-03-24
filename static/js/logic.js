// FILTER FUNCTIONS ______________________________________________________________________________
//get current date
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
  newdate.setHours(0, 0, 0, 0);
  return newdate
}

// find the button (id in HTML is filter-btn)
var button = d3.select("#filter");

// find the form (id in HTML is form-group)
var form = d3.select("#form-group");

var fireData = []
// d3.json("http://127.0.0.1:5000/api/v1.0/fire", function(response) {
d3.json("https://california-disasters.herokuapp.com/api/v1.0/fire", function(response) {
  for (var i =0; i < response["data"].length; i++) {
    fireData.push(response["data"][i]["properties"])
  }
});

var earthquakeData = []
// d3.json("http://127.0.0.1:5000/api/v1.0/earthquake", function(response) {
d3.json("https://california-disasters.herokuapp.com/api/v1.0/earthquake", function(response) {
  for (var i =0; i < response["data"].length; i++) {
    earthquakeData.push(response["data"][i]["properties"])
  }
});

// set filtered data to default values
var filteredFire = fireData // add default values
var filteredEarthquake = earthquakeData // add default values

// INITIALIZE COUNTIES MAP ______________________________________________________________________________
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

// Initialize earthquake data


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
  var inputValue_fire = inputElement_excludeFire.property("checked");
  var inputValue_earthquake = inputElement_excludeEarthquake.property("checked");

  // reset the data before aplying filters
  var filteredFire = fireData
  var filteredEarthquake = earthquakeData

  if (!inputValue_start) {

    // console.log(inputValue_start + "Is NULL")
    filteredFire = filteredFire.filter(data => formatDate(data.date_cre) >= formatDate("01/01/2013"));
    filteredEarthquake = filteredEarthquake.filter(data => formatDate(data["epoch_time"]) >= formatDate("01/01/2013"));
    
  }
  else {

    filteredFire = filteredFire.filter(data => formatDate(data["date_cre"]) >= formatDate(inputValue_start));
    filteredEarthquake = filteredEarthquake.filter(data => formatDate(data["epoch_time"]) >= formatDate(inputValue_start));
    // console.log(inputValue_start + "Is NOT NULL")

  };

  if (!inputValue_end) {

    filteredFire = filteredFire.filter(data => formatDate(data.date_cre)  < formatDate(getToday()));
    filteredEarthquake = filteredEarthquake.filter(data => formatDate(data["epoch_time"]) <= formatDate(getToday()));

  }
  else {

    filteredFire = filteredFire.filter(data => formatDate(data.date_cre)  < formatDate(inputValue_end));
    filteredEarthquake = filteredEarthquake.filter(data => formatDate(data["epoch_time"]) <= formatDate(inputValue_end));

  };

  if (!inputValue_fire){

    // console.log("fire checkbox is:" + inputValue_fire)
    filteredFire = {}

  };

  if (!inputValue_earthquake) {

    // console.log("fire checkbox is:" + inputValue_fire)
    filteredEarthquake = {}

  };


  updateVisualizations(filteredFire, filteredEarthquake)
};

// DANGER POINTS FUNCTION _______________________________________________________________________

function dangerScores(filtered_Fire, filtered_Earthquake){
  firescores = d3.csv("../../data/fire_danger_csv.csv");
  // earthquakescores = d3.csv("../../data/earthquake_danger_csv.csv")
  
  //figure out a way to convert the CSVs to python functions that can be ran via javascript
  //or just keep this part static if there isn't time -low priority

  var array = {}

  for (i=0; i < filtered_Fire.length; i++){
    // var dict = {}
    for (j=0; j < firescores.length; j++){
      if (filtered_Fire[i]["name"] === firescores[j]["name"] && filtered_Fire[i]["county"] === firescores[j]["fire_danger_score"]){
          // filteredFire[i]["score"] === firescores[j]["fire_danger_score"]
          // dict["Id"] = filtered_Fire[i]["county"]
          // dict["score"] = firescores[j]["fire_danger_score"]
          if (array.hasOwnProperty(filtered_Fire[i]["county"])) {
            array[filtered_Fire[i]["county"]] = array[filtered_Fire[i]["county"]] + parseInt(firescores[j]["fire_danger_score"])
          }
          else {
            array[filtered_Fire[i]["county"]] = parseInt(firescores[j]["fire_danger_score"])

          };
      };
    };
  };

  //groupby county and find the sum, populate 2 arrays 
  // array.reduce(function(res, value) {
  //   if (!res[value.Id]) {
  //     res[value.Id] = { Id: value.Id, score: 0 };
  //     result.push(res[value.Id])
  //   }
  //   res[value.Id].score += value.score;
  //   return res;
  // }, {});
  

  var county = Object.keys(array);
  var score = Object.values(array);

  return county, score
};

// CREATE FIRE MAP ______________________________________________________________________________
function fireMap(fire_Data) {
var heatArray=[];

for (i=0; i< fire_Data.length; i++) {
  // console.log(fire_Data[i])
  heatArray.push([fire_Data[i]["lat"],filteredFire[i]["lng"]])
}
// console.log(heatArray);
var heat= L.heatLayer(heatArray,{
  radius: 20,
  blur:2
}).addTo(myMap);

};

// CREATE EARTHQUAKE MAP ________________________________________________________________________
function earthquakeMap(earthquake_Data) {
  for (var i =0; i < earthquake_Data.length; i++) {
    
    var lat = earthquake_Data[i]["latitude"];
    var long = earthquake_Data[i]["longitude"];
    var depth = earthquake_Data[i]["depth(km)"];
    var size = earthquake_Data[i]["magnitude"];
    var loc = earthquake_Data[i]["location"];

    if (size <= 5.9 && size > 5) {
      var earthquakeIcon = L.icon({
        iconUrl:'static/js/icons/earthquake_icon_green.svg',
        iconSize: [32,32]
      })
      var popupText = "(Moderate)"
    }
    else if (size <= 6.9 && size > 5.9) {
      var earthquakeIcon = L.icon({
        iconUrl:'static/js/icons/earthquake_icon_yellow.svg',
        iconSize: [32,32]
      })
      var popupText = "(Strong)"
    }
    else if (size <= 7.9 && size > 6.9) {
      var earthquakeIcon = L.icon({
        iconUrl:'static/js/icons/earthquake_icon_orange.svg',
        iconSize: [32,32]
      })
      var popupText = "(Major)"
    }
    else if (size > 7.9) {
      var earthquakeIcon = L.icon({
        iconUrl:'static/js/icons/earthquake_icon_red.svg',
        iconSize: [32,32]
      })
      var popupText = "(Great)"
    }
    
    // Check for location property
    if (size >= 5) {
      var location = [lat, long];
      // create marker
      var markerLayer = L.marker(location, {
        icon:earthquakeIcon,
      })
        .bindPopup(
          "<h3>Location: " + loc +
            "</h3><h4>Magnitude: " +
            size + " " + popupText +
            "<br>Depth: " +
            depth +
            "km</h4>"
        )
        .addTo(myMap);
    }
  }
};

// CREATE BAR CHART _____________________________________________________________________________
function plotBarChart(filtered_Fire, filtered_Earthquake) {
  // // get data
  // [counties, points] = dangerScores(filtered_Fire, filtered_Earthquake)
  var counties = ["Ventura", "Tehama", "Riverside", "Lassen", "Los Angeles", "Yolo", "Santa Cruz", "San Mateo", "Nevada", "Kings"]
  var fire_scores = [926.6666667,926.6666667,3153.333333,1393.333333,1286.666667,180,66.66666667,73.33333333, 93.33333333,80]
  var other_scores = [12,12,42,19,17,2,1,1,1,1]
  // var trace1 = {
  //   x: counties,
  //   y: points,
  //   type: "bar"
  // };

  // var data = [trace1];

  // var layout = {
  //   title: "'Bar' Chart"
  // };

  // Plotly.newPlot("chartid", data, layout);

  var options = {
    chart: {
      //renderTo: '#stackedbarchart',
      type: 'bar'
    },
    title: {
      text: 'Top 5 Disastrous Counties in California'
    },
    xAxis: {
      categories: ["fire severity score", "fire count"],
      title: {
        text: null
      }
    },
    yAxis: {
      min: 0,
      title: {
        text: 'Fire Danger Score',
        align: 'high'
      },
      labels: {
        overflow: 'justify'
      }
    },
    tooltip: {
      valueSuffix: ''
    },
    plotOptions: {
      bar: {
        dataLabels: {
          enabled: true
        }
      }
    },
    legend: {
      layout: 'vertical',
      align: 'right',
      verticalAlign: 'top',
      x: -40,
      y: 80,
      floating: true,
      borderWidth: 1,
      backgroundColor: '#FFFFFF',
      shadow: true
    },
    credits: {
      enabled: false
    },
    series: [{
      name: counties[0],
      data: [fire_scores[0], other_scores[0]]
    }, {
      name: counties[1],
      data: [fire_scores[1], other_scores[1]]
    }, {
      name: counties[2],
      data: [fire_scores[2], other_scores[2]]
    }, {
      name: counties[3],
      data: [fire_scores[3], other_scores[3]]
    }, {
      name: counties[4],
      data: [fire_scores[4], other_scores[4]]
    },{
      name: counties[5],
      data: [fire_scores[5], other_scores[5]]
    }, {
      name: counties[6],
      data: [fire_scores[6], other_scores[6]]
    }, {
      name: counties[7],
      data: [fire_scores[7], other_scores[7]]
    }, {
      name: counties[8],
      data: [fire_scores[8], other_scores[8]]
    }, {
      name: counties[9],
      data: [fire_scores[9], other_scores[9]]
    }]
  };

  Highcharts.chart('stackedbarchart',options);


};

// FUNCTION TO UPDATE VISUALIZATIONS ____________________________________________________________
function updateVisualizations(filtered_Fire, filtered_Earthquake) {
  // [filtered_Fire, filtered_Earthquake] = filterData()
  // myMap.clearLayers();

  myMap.eachLayer(function (layer) {myMap.removeLayer(layer);});
  
  console.log("fire data: ")
  console.log(filtered_Fire)
  console.log("earthquake data: ")
  console.log(filtered_Earthquake)

  // Add Map
  // var myMap = L.map("mapid", {
  //   center: [36.7783, -119.4179],
  //   zoom: 5
  // });
  
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
  
  // Update Fire Map
  fireMap(filtered_Fire)

  // Run danger scorer
  // [county_names, danger_score] = dangerScores(filtered_Fire, filtered_Earthquake)
  // console.log("county name: ")
  // console.log(county_names)
  // console.log("danger score: ")
  // console.log(danger_score)

  // Update Earthquake Map
  earthquakeMap(filtered_Earthquake)

  // Update Bar Chart
  plotBarChart(filtered_Fire, filtered_Earthquake)

};

// CALL THE FUNCTIONS ___________________________________________________________________________
  fireMap(filteredFire)
  earthquakeMap(filteredEarthquake)
  // plotBarChart(filteredFire, filteredEarthquake)

// D3 Listener __________________________________________________________________________________
button.on("click", filterData);
form.on("submit",filterData);
