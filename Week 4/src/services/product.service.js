const productRepo = require("../repositories/product.repository");

class ProductService{
    async getProducts(query){
        const{
            search,
            minPrice,
            maxPrice,
            sort,
            page=1,
            limit=10,
            includeDeleted,
            tags,
        } =query;
        const filter = {};
        if(!includeDeleted){
            filter.deletedAt = null;
        }

        if(search){
            filter.$or = [
                {name: {$regex: search, $options: "i"}},
                {description:{$regex: search,$options: "i"}},
            ];
        }
        if(minPrice || maxPrice){
            filter.price={};
            if(minPrice) filter.price.$gte=Number(minPrice);
            if(maxPrice) filter.price.$lte=Number(maxPrice);
        }
        if(tags){
            filter.tags = {$in: tags.split(",")};
        }

        const sortOptions ={};
        if(sort){
            const [field,direction]=sort.split(":");
            sortOptions[field] = direction ==="desc"?-1:1;
        }

        const skip =(page-1)*limit;

        const data = await productRepo.find(filter,{
            sort : sortOptions,
            skip,
            limit: Number(limit),
        });

        const total = await productRepo.count(filter);

        return{
            data,
            total,
            page: Number(page),
            limit: Number(limit),
        };
    }

    async softDelete(id){
        return productRepo.update(id,{deletedAt: new Date()});
    }
}
module.exports =new ProductService();