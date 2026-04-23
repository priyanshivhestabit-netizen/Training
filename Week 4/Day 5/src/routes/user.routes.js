const express = require("express");
const User = require("../models/Account");
const router = express.Router();

const validate = require("../middlewares/validate");
const userSchema = require("../validations/user.validation");

const { registerUser } = require("../controllers/account.controller");

router.post(
  "/",
  validate(userSchema),
  registerUser
);
// GET ALL USERS
router.get("/", async (req, res) => {
  const users = await User.find();
  res.json(users);
});

// GET SINGLE USER
router.get("/:id", async (req, res) => {
  const user = await User.findById(req.params.id);

  if (!user) {
    return res.status(404).json({ message: "User not found" });
  }

  res.json(user);
});
module.exports = router;