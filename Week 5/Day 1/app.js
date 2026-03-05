const http  = require('http');

const server = http.createServer((req,res)=>{
    res.end("Docker Day 1 is running");
})

server.listen(3000,()=>{
    console.log("server running on port 3000");
});