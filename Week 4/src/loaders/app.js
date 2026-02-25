const express = require("express");
const logger =require("../utils/logger");

const productController = require("../controllers/product.controller");
const errorMiddleware = require("../middlewares/error.middleware");

const seedRoutes = require("../routes/seed.routes");

function loadApp(){
    const app = express();

    //middlewares
    app.use(express.json());
    logger.info("Middlewares loaded");

    //routes
    app.get("/health",(req,res)=>{
        res.json({status:"OK"});
    });

    // Product routes
    app.get("/products", productController.getProducts);
    app.delete("/products/:id", productController.deleteProduct);   
    
    if(process.env.NODE_ENV === "development"){
        app.use(seedRoutes);
    }
    app.use(errorMiddleware);
    logger.info("Routes mounted");
    return app;
}

module.exports = loadApp;