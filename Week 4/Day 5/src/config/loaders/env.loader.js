const dotenv = require("dotenv");
const path = require("path");

function loadEnv(){
    const env= process.env.NODE_ENV || "dev";

    const envFile=`.env.${env}`;
    const envPath=path.resolve(process.cwd(),envFile);

    dotenv.config({path: envPath});
    console.log(`Loaded environment: ${envFile}`);
}

module.exports = {loadEnv};