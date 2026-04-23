const express = require("express");
const os = require("os");

const app = express();

app.get("/api", (req,res)=>{
  res.json({
    message:"Response from backend",
    container: os.hostname()
  });
});

app.listen(3000, ()=>{
  console.log("Server running on port 3000");
});