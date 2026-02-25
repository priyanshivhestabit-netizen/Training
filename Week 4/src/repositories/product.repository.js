const Product  =require("../models/Products");

class ProductRepository {
    async create(data){
        return Product.create(data);
    }

    async find(filter,options){
        return Product.find(filter)
            .sort(options.sort)
            .skip(options.skip)
            .limit(options.limit);
    }

    async count(filter){
        return Product.countDocuments(filter);
    }

    async update(id,data){
        return Product.findByIdAndUpdate(id, data, {new:true});
    }
}

module.exports = new ProductRepository();