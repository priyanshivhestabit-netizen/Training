const express = require("express");
const User =  require("../models/Account");
const router = express.Router();
const validate = require("../middlewares/validate")
const userSchema = require("../validations/user.validation");

router.post(
    "/users",
    validate(userSchema),
    async(req,res)=>{
        try{
            const user = await User.create(req.body);
            res.status(201).json(user);
        }
        catch(error){
            res.status(500).json({message:error.message});
        }
        
    }
);

module.exports = router;