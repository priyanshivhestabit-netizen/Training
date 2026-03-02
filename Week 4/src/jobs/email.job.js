const { Queue } = require("bullmq");
const connection = require("../utils/redis");

const emailQueue = new Queue("emailQueue", { connection });

const addEmailJob = async (data) => {
  console.log("Adding job to queue..."); // ADD THIS
  await emailQueue.add("sendEmail", data);
  console.log("Job successfully added");  // ADD THIS
};

module.exports = { addEmailJob };