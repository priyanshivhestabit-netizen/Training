const Product  =require("../models/Products");

class ProductRepository {
    async create(data){
        return Product.create(data);
    }

    async find(filter, options = {}) {
    const {
        sort = {},
        skip = 0,
        limit = 10
    } = options;

    console.log("LIMIT:", limit);
    console.log("SKIP:", skip);

    return Product.find(filter)
        .sort(sort)
        .skip(skip)
        .limit(limit);
}
    
    async count(filter){
        return Product.countDocuments(filter);
    }

    async update(id,data){
        return Product.findByIdAndUpdate(id, data, {new:true});
    }
}

module.exports = new ProductRepository();