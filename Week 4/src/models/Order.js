const mongoose = require("mongoose");

const orderSchema = new mongoose.Schema(
    {
        account:{
            type:mongoose.Schema.Types.ObjectId,
            ref:"Account",
            required:true,
            index:true
        },
        amount:{
            type:Number,
            required:true,
            min:0
        },
        status:{
            type:String,
            enum: ["pending","completed","cancelled"],
            default:"pending"
        },
        expiresAt:{
            type: Date
        }
    },
    {
        timestamps:true
    }
);

//ttl index(auto delete expired orders)
orderSchema.index({expiresAt:1},{expireAfterSeconds:0});

//compound index
orderSchema.index({status:1,createdAt:-1});
module.exports = mongoose.model("Order",orderSchema);