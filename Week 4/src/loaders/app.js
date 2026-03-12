const express = require("express");
const logger = require("../utils/logger");

const errorMiddleware = require("../middlewares/error.middleware");
const securityMiddleware = require("../middlewares/security");
const tracingMiddleware = require("../utils/tracing");

const seedRoutes = require("../routes/seed.routes");
const productRoutes = require("../routes/product.routes");
const userRoutes = require("../routes/user.routes");

const swaggerLoader = require("./swagger");

function loadApp() {
  const app = express();

  // 🔹 1. Core middlewares
  app.use(express.json({ limit: "10kb" }));
  logger.info("JSON Middleware loaded");

  // 🔹 2. Security middlewares (Helmet, CORS, Rate limit)
  securityMiddleware(app);
  logger.info("Security middlewares loaded");

  // 🔹 3. Request tracing 
  app.use(tracingMiddleware);
  logger.info("Tracing middleware loaded");

  // 🔹 4. Health check
  app.get("/health", (req, res) => {
    res.json({ status: "OK" });
  });

  app.get("/debug", (req, res) => {
  res.send("Debug route working");
});
  // 🔹 5. Routes
  app.use("/products", productRoutes);
  app.use("/users", userRoutes);

  if (process.env.NODE_ENV === "development") {
    app.use("/seed", seedRoutes);
  }

  logger.info("Routes mounted");

  // 🔹 6. Swagger (after routes)
  swaggerLoader(app);
  logger.info("Swagger documentation loaded");

  // 🔹 7. Error middleware (ALWAYS LAST)
  app.use(errorMiddleware);

  return app;
}

module.exports = loadApp;