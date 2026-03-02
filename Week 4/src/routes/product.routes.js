const express = require("express");
const router = express.Router();
const Product = require("../models/Products")

const validate  = require("../middlewares/validate");
const {
  createProductSchema,
  productQuerySchema,
  idParamSchema
} = require("../validations/product.validation");

router.delete("/:id", async (req, res) => {
  const product = await Product.findByIdAndUpdate(
    req.params.id,
    { deletedAt: new Date() },
    { new: true }
  );

  if (!product) {
    return res.status(404).json({ message: "Product not found" });
  }

  res.json(product);
});
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