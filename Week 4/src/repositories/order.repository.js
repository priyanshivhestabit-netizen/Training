const Order = require("../models/Order");

class OrderRepository{
    async create(data){
        return Order.create(data);
    }

    async findByAccount(accountId){
        return (await Order.find({account: accountId})).toSorted({ createdAt: -1});
    }

    async findPaginated({page=1,limit=10,status}){
        const query = {};
        if(status) query.status = status;
        const skip = (page-1)*limit;
        const data = await Order.find(query)
            .sort({createdAt: -1})
            .skip(skip)
            .limit(limit);

        const total = await Order.countDocuments(query);
        return{
            data,
            total,
            page,
            pages: Math.ceil(total/limit)
        };
    }
    async delete(id){
        return Order.findByIdAndDelete(id);
    }
}
module.exports =new OrderRepository();