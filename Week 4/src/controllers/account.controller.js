const AccountService = require("../services/account.service");
const { addEmailJob } = require("../jobs/email.job");
const logger = require("../utils/logger");

exports.registerUser = async (req, res) => {
  try {
    console.log("Register controller hit");

    const user = await AccountService.create(req.body);

    console.log("Adding job to queue...");
    await addEmailJob({
      email: user.email,
      name: user.name,
    });
    console.log("Job successfully added");

    logger.info({
      requestId: req.requestId,
      message: `User registration completed. Email sent to ${user.email}`,
    });

    return res.status(201).json({
      success: true,
      message: `User created. Email will be sent to ${user.email}`,
    });

  } catch (error) {
    console.error("Controller error:", error);
    return res.status(500).json({
      success: false,
      message: "Internal server error",
    });
  }
};