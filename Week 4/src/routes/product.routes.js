const express = require("express");
const router = express.Router();
const Product = require("../models/Products")

const validate  = require("../middlewares/validate");
const {
  createProductSchema,
  productQuerySchema,
  idParamSchema
} = require("../validations/product.validation");

router.post(
  "/products",
  validate(createProductSchema, "body"),
  async (req, res) => {
    const product = await Product.create(req.body);
    res.json(product);
  }
);

router.get(
  "/products",
  validate(productQuerySchema, "query"),
  async (req, res) => {

    const { search, sort, order, includeDeleted } = req.query;

    let filter = {};

    if (includeDeleted !== "true") {
      filter.deletedAt = null;
    }

    if (search) {
      filter.name = { $regex: search, $options: "i" };
    }

    let query = Product.find(filter);

    if (sort) {
      query = query.sort({
        [sort]: order === "desc" ? -1 : 1
      });
    }

    const products = await query;

    res.json(products);
  }
);

module.exports = router;