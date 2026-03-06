const express = require('express');
const mongoose = require('mongoose');
const cors = require('cors');

const app = express();

app.use(cors());
app.use(express.json());

mongoose.connect("mongodb://mongo:27017/devopsdb")
.then(()=> console.log("MongoDB connected"))
.catch(err=> console.log(err));

app.get("/api",(req,res)=>{
    res.json({message: "Backend running inside docker"});
});

app.listen(5000,()=>{
    console.log("server running on port 5000 ");
});