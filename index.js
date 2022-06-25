//

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

const port = process.env.PORT || 3000;

// Start listening to server
app.listen(port, () => {
  console.log(`Listening on port ${port}`);
});
