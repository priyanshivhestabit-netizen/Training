const Account = require("../models/Account");

class AccountRepository{
    async create(data){
        return Account.create(data);
    }

    async findById(id){
        return Account.findById(id).select("-password");
    }

    async findPaginated({page=1, limit=10, status}){
        const query ={};
        if(status){
            query.status =status;
        }
        const skip = (page-1)*limit;

        const data = await Account.find(query)
            .sort({createdAt: -1})
            .skip(skip)
            .limit(limit)
            .select("-password");

        const total = await Account.countDocuments(query);

        return{
            data,
            total,
            page,
            pages: Math.ceil(total/limit)
        };
    }

    async update(id,updateData){
        return Account.findByIdAndUpdate(id,updateData,{
            new:true,
            runValidators: true
        });
    }
    async delete(id){
        return Account.findByIdAndDelete(id);
    }
}
module.exports = new AccountRepository();