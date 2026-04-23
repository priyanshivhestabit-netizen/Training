const pino = require("pino");
const fs = require("fs");
const path = require("path");

const logDir = path.join(__dirname, "../../logs");

if (!fs.existsSync(logDir)) {
  fs.mkdirSync(logDir, { recursive: true });
}

const fileStream = fs.createWriteStream(
  path.join(logDir, "app.log"),
  { flags: "a" }
);

const logger = pino(
  {
    level: "info"
  },
  pino.multistream([
    { stream: process.stdout }, // console
    { stream: fileStream }      // file
  ])
);

module.exports = logger;