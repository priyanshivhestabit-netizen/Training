const express = require('express');
const mongoose = require('mongoose');
const os = require('os');

const app = express();

mongoose.connect(process.env.MONGO_URI)
.then(()=>console.log("Mongo connected"));

app.get("/api", (req,res)=>{
    res.json({
        message: "Backend working",
        container: os.hostname()
    });
});

app.get("/health", (req,res)=>{
    res.status(200).send("OK");
});

app.listen(3000,()=>{
    console.log("server is running on port 3000.");
});