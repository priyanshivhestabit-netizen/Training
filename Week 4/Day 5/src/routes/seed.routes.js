const express = require ("express");
const Account = require("../models/Account");
const Order = require("../models/Order");
const Product = require("../models/Products");
const router = express.Router();

    //temp seed route
router.get("/seed/account",async(req,res)=>{
    try{
        const account =await Account.create({
            firstName:"Priyanshi",
            lastName:"Verma",
            email:"priyanshiv@gmail.com",
            password:"123456"
        });
        res.json(account);
    }catch(error){
        res.status(500).json({error:error.message});
    }
});

    // temp order seed route
router.get("/seed-order/order", async (req, res) => {
    try {
        const account = await Account.findOne();

        if (!account) {
            return res.status(400).json({ error: "No account found. Seed account first." });
        }

        const order = await Order.create({
            account: account._id,
            amount: 999,
            expiresAt: new Date(Date.now() + 60000) // expires in 1 minute
        });

        res.json(order);
        } 
        catch (error) {
            res.status(500).json({ error: error.message });
        }
});

//product seed
router.get("/seed-product/product", async(req,res)=>{
    try{
        const products = await Product.insertMany([
            {
                name: "iPhone 15",
                description: "Apple smartphone",
                price: 50000,
                tags: ["apple","phone"]
            },
            {
                name: "Samsung Galaxy",
                description: "Samsung smartphone",
                price: 510000,
                tags: ["samsung","phone"]
            }
        ]);
        res.json(products);
    }
    catch(error){
        res.status(500).json({error:error.message});
    }
});

router.delete("/products/:id", async (req, res) => {
  try {
    const product = await Product.findByIdAndUpdate(
      req.params.id,
      { deletedAt: new Date() },
      { new: true }
    );

    if (!product) {
      return res.status(404).json({ message: "Product not found" });
    }

    res.json({
      success: true,
      message: "Product soft deleted",
      data: product
    });

  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

router.get("/products", async (req, res) => {
  try {
    const { includeDeleted } = req.query;

    let filter = {};

    if (includeDeleted !== "true") {
      filter.deletedAt = null;
    }

    const products = await Product.find(filter);

    res.json({
      success: true,
      count: products.length,
      data: products
    });

  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

module.exports = router;
