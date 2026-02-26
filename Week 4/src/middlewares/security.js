const helmet = require("helmet");
const cors = require("cors");
const rateLimit = require("express-rate-limit");
const mongoSanitize = require("express-mongo-sanitize");
const hpp = require("hpp");
const express = require("express");

const securityMiddleware = (app) => {
    //secure http headers
    app.use(helmet());

    //cors
    app.use(cors({
        origin: "http://localhost:3000",
        methods: ["GET","POST","PUT","DELETE"]
    }));

    const limiter = rateLimit({
        windowMs: 15 * 60 * 1000,
        max:100,
        message: "Too many requests from this IP, try again later."
    });

    app.use(limiter);

    //prevent noSQL injection
    app.use((req, res, next) => {
  req.body = mongoSanitize.sanitize(req.body);
  next();
});

    //prevent parameter pollution
    app.use(hpp());

    //limit body size
    app.use(express.json({limit:"10kb"}));
};

module.exports = securityMiddleware;