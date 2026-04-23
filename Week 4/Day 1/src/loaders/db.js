const mongoose = require("mongoose");
const logger = require("../utils/logger");

async function connectDB(){
    try{
        await mongoose.connect(process.env.MONGO_URI);
        logger.info("Database connected");
    }
    catch(error){
        logger.error("Database connection failed");
        process.exit(1);
    }
}

module.exports = connectDB;