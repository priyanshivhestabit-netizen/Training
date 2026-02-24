const express = require("express");
const logger =require("../utils/logger");
const Account = require("../models/Account");
const Order=require("../models/Order");

function loadApp(){
    const app = express();

    //middlewares
    app.use(express.json());
    logger.info("Middlewares loaded");

    //routes
    app.get("/health",(req,res)=>{
        res.json({status:"OK"});
    });
    
    if(process.env.NODE_ENV === "development"){

    
    //temp seed route
    app.get("/seed",async(req,res)=>{
        try{
            const account =await Account.create({
                firstName:"Priyanshi",
                lastName:"Verma",
                email:"priyanshiv@gmail.com",
                password:"123456"
            });
            res.json(account);
        }catch(error){
            res.status(500).json({error:error.message});
        }
    });

    // temp order seed route
    app.get("/seed-order", async (req, res) => {
        try {
            const account = await Account.findOne();

            if (!account) {
            return res.status(400).json({ error: "No account found. Seed account first." });
            }

            const order = await Order.create({
            account: account._id,
            amount: 999,
            expiresAt: new Date(Date.now() + 60000) // expires in 1 minute
            });

            res.json(order);
            } catch (error) {
            res.status(500).json({ error: error.message });
        }
    });

}

    logger.info("Routes mounted: 1 endpoint");
    return app;
}

module.exports = loadApp;