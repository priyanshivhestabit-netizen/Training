const { Worker } = require("bullmq");
const redis = require("../utils/redis");
const logger = require("../utils/logger");

const worker = new Worker(
  "emailQueue",
  async (job) => {
    logger.info(`Processing job ${job.id}`);
    console.log("Email sent to:", job.data.email);
  },
  { connection: redis }
);

worker.on("completed", (job) => {
  logger.info(`Job ${job.id} completed`);
});

worker.on("failed", (job, err) => {
  logger.error(`Job ${job.id} failed: ${err.message}`);
});