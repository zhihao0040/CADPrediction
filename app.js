const express = require("express");
const bodyParser = require("body-parser");
const request = require("request");


const app = express();

app.use(bodyParser.urlencoded({ extended: false, }));
app.use(express.static("public"));



app.get("/", function (req, res) {
    res.sendFile(__dirname + "/home.html");
})

app.post("/", function(req,res){
    console.log(req.body);
    res.redirect("/about")
})

app.get("/about", function (req, res) {
    res.sendFile(__dirname + "/about.html");
})


app.get("/api", function (req, res) {
    res.sendFile(__dirname + "/api.html");
})


app.listen(3000, function () {
    console.log("Listenning at port 3000");
});