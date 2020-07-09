const express = require("express");
const bodyParser = require("body-parser");

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

// set port, listen for requests
app.listen(3000, () => {
  console.log("Server is running on port 3000.");
});