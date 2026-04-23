const express = require("express");
const router = express.Router();
const Product = require("../models/Products")
const productController = require("../controllers/product.controller");

const validate  = require("../middlewares/validate");
const {
  createProductSchema,
  productQuerySchema,
  idParamSchema
} = require("../validations/product.validation");

router.delete(
  "/:id",
  validate(idParamSchema, "params"),
  productController.deleteProduct
);

router.post(
  "/",
  validate(createProductSchema, "body"),
  async (req, res) => {
    const product = await Product.create(req.body);
    res.json(product);
  }
);

router.get(
  "/",
  validate(productQuerySchema, "query"),
  productController.getProducts
);

module.exports = router;