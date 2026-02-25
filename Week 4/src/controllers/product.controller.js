const productService = require("../services/product.service");

exports.getProducts = async (req,res,next) => {
    try{
        const result = await productService.getProducts(req.query);
        res.json({success: true, ...result});
    }
    catch(err){
        next(err);
    }
};

exports.deleteProduct = async (req,res,next)=>{
    try{
        const product  = await productService.softDelete(req.params.id);
        res.json({success:true, data:product});
    }
    catch(err){
        next(err);
    }
};