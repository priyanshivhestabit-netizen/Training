const Joi = require("joi");

const userSchema = Joi.object({
    firstName: Joi.string()
        .min(2)
        .required(),
    lastName: Joi.string()
        .min(2)
        .required(),

    email: Joi.string()
        .email()
        .required(),
    password: Joi.string()
        .min(6)
        .required()
});

module.exports = userSchema;