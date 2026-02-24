const express = require("express");
const logger =require("../utils/logger");

function loadApp(){
    const app = express();

    //middlewares
    app.use(express.json());
    logger.info("Middlewares loaded");
    
    //routes
    app.get("/health",(req,res)=>{
        res.json({status:"OK"});
    });

    logger.info("Routes mounted: 1 endpoint");
    return app;
}

module.exports = loadApp;