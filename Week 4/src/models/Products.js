const mongoose = require("mongoose");

const productSchema = new mongoose.Schema(
    {
        name: {
            type: String,
            required: true,
            trim: true,
        },
        description: String,
        price: {
            type: Number,
            required: true,
            min: 0,
        },
        tags: [String],
        deletedAt: {
            type: Date,
            default: null,
        },
    },
    {timestamps: true}
);
module.exports = mongoose.model("Product", productSchema);