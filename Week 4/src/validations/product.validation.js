const Joi = require("joi");

// Create Product
const createProductSchema = Joi.object({
  name: Joi.string().min(3).max(100).required(),
  description: Joi.string().max(500).required(),
  price: Joi.number().positive().required(),
  tags: Joi.array().items(Joi.string()).optional()
});


// Query Validation
const productQuerySchema = Joi.object({
  search: Joi.string().optional(),
  sort: Joi.string().valid("price", "name", "createdAt").optional(),
  order: Joi.string().valid("asc", "desc").optional(),
  includeDeleted: Joi.string().valid("true", "false").optional()
});

// Param Validation
const idParamSchema = Joi.object({
  id: Joi.string().length(24).hex().required()
});

module.exports = {
  createProductSchema,
  productQuerySchema,
  idParamSchema
};