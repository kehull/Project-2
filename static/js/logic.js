// Creating map object
var myMap = L.map("mapid", {
  center: [40.7, -73.95],
  zoom: 11
});

// Adding tile layer to the map
L.tileLayer("https://api.mapbox.com/styles/v1/{id}/tiles/{z}/{x}/{y}?access_token={accessToken}", {
  attribution: "© <a href='https://www.mapbox.com/about/maps/'>Mapbox</a> © <a href='http://www.openstreetmap.org/copyright'>OpenStreetMap</a> <strong><a href='https://www.mapbox.com/map-feedback/' target='_blank'>Improve this map</a></strong>",
  tileSize: 512,
  maxZoom: 18,
  zoomOffset: -1,
  id: "mapbox/streets-v11",
  accessToken: API_KEY
}).addTo(myMap);

// Store API query variables
// var baseURL = "https://earthquake.usgs.gov/fdsnws/event/1/query?format=geojson";
// var dates = "&starttime=2014-01-01&endtime=2014-01-02";
// var minmagnitude = "&minmagnitude=5";
// var limit = "&$limit=10000";

// Assemble API query URL
var url = 'https://earthquake.usgs.gov/fdsnws/event/1/query?format=geojson&starttime=2013-01-01&endtime=2021-03-12&minmagnitude=5'

// Grab the data with d3
d3.json(url, function(response) {

  // Create a new marker cluster group
  var markers = L.markerClusterGroup();

  // Loop through data
  for (var i = 0; i < response['features'].length; i++) {

    // Set the data location property to a variable
    var location = response['features']['properties'][i]['geometry'];

    // Check for location property
    if (location) {

      // Add a new marker to the cluster group and bind a pop-up
      markers.addLayer(L.marker([location['coordinates'][1], location['coordinates'][0]])
        .bindPopup(response['features']['properties'][i]['place']));
    }

  }

  // Add our marker cluster layer to the map
  myMap.addLayer(markers);

});
