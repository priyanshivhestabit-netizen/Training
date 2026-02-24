const mongoose  =require("mongoose");
const bcrypt = require("bcrypt");

const accountSchema = new mongoose.Schema(
    {
    firstName: {
        type:String,
        required:true,
        trim:true
    },
    lastName:{
        type:String,
        required:true,
        trim:true
    },
    email:{
        type:String,
        required:true,
        unique:true,
        lowecase:true,
        index:true
    },
    password:{
        type:String,
        required:true,
        minlength:6
    },
    status:{
        type:String,
        enum: ["active","inactive","suspended"],
        default:"active"
    }
},
{
    timestamps:true
}
);

//virtual field

accountSchema.virtual("fullName").get(function(){
    return `${this.firstName} ${this.lastName}`;
});

//compound index
accountSchema.index({ status:1, createdAt: -1});

//pre-save hook(hash password)
accountSchema.pre("save", async function(next){
    if(!this.isModified("password")) return next();

    const salt = await bcrypt.genSalt(10);
    this.password = await bcrypt.hash(this.password,salt);

});

module.exports = mongoose.model("Account",accountSchema);