firescores = d3.csv("../../data/fire_danger_csv.csv");

var filtered_Fire = []
d3.json("http://127.0.0.1:5000/api/v1.0/fire", function(response) {
  for (var i =0; i < response["data"].length; i++) {
    fireData.push(response["data"][i]["properties"])
  }
});

var results = {}

for (i=0; i < filtered_Fire.length; i++){
  // var dict = {}
  for (j=0; j < firescores.length; j++){
    if (filtered_Fire[i]["name"] === firescores[j]["name"] && filtered_Fire[i]["county"] === firescores[j]["county"]){
        if (results.hasOwnProperty(filtered_Fire[i]["county"])) {
            results[filtered_Fire[i]["county"]] += parseInt(firescores[j]["fire_danger_score"])
        }
        else {
            results[filtered_Fire[i]["county"]] = parseInt(firescores[j]["fire_danger_score"])
        };
    };
  };
};

var county = Object.keys(results);
var score = Object.values(results);

// console.log(county)
// console.log(score)