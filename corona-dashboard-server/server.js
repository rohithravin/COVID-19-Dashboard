const express = require("express");
const bodyParser = require("body-parser");
const {spawn} = require('child_process');
const userLocationRouter = require('./routes/user-location-route')

const app = express();

// parse requests of content-type: application/json
app.use(bodyParser.json());

// parse requests of content-type: application/x-www-form-urlencoded
app.use(bodyParser.urlencoded({ extended: true }));

app.use(userLocationRouter);

// simple route
app.get("/", (req, res) => {
  res.json({ message: "Welcome to COVID-19 Dashboard Server." });
});

runLoadDataScript();


function runLoadDataScript(){
  const subprocess =  spawn('python', ["-u", './scripts/load-data.py']);
  
  // print output of script
  subprocess.stdout.on('data', (data) => {
    console.log(`data:${data}`);
  });
  subprocess.stderr.on('data', (data) => {
    console.log(`error:${data}`);
  });
  subprocess.on('close', () => {
    console.log("Closed");

});

}



setInterval(function() {
  runLoadDataScript();
}, 1440 * 60 * 1000);





// set port, listen for requests
app.listen(3000, () => {
  console.log("Server is running on port 3000.");
});