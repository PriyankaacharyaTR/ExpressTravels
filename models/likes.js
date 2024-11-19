const mongoose = require("mongoose");
const Schema = mongoose.Schema;


// Define the schema
const likeSchema = new Schema({
    schema:{type:String},
    id:{type:String}
});

// Create a model from the schema
const Like = mongoose.model('Like', likeSchema);

module.exports = Like;

