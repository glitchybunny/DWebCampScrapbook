/*

    A local web app that allows images to be uploaded into a scrapbook on archive.org
    Author: Glitch Taylor (https://rtay.io/)

 */

// Initialise express server
const dotenv = require("dotenv");
dotenv.config("./.env");
const morgan = require("morgan");
const express = require("express");
const app = express();

if (process.env.NODE_ENV === "development") {
  app.use(morgan("dev"));
} else {
  app.use(morgan("short"));
}
app.use(express.json());
app.use(express.urlencoded({ extended: true }));
app.use(express.static("./www"));

const port = process.env.PORT || 3000;

// Start listening to server
app.listen(port, () => {
  console.log(`Listening on port ${port}`);
});
