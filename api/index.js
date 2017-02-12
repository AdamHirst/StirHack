var express = require('express');
var app = express();
var bodyParser = require('body-parser')
const MongoClient = require('mongodb').MongoClient

app.use(bodyParser.json())

app.get('/', function (req, res) {
   res.send('Hello World');
})

// Register a new store 
app.post('/store', function (req, res) {
	console.log(req.body["test"])
	res.send("Done")
})

app.post('/store/newcamera', function (req, res) {
	// Add camera to store
	var store = res.body["store_id"]

	res.send({"camera_id": 34})
})

var server = app.listen(8081, function () {
   var host = server.address().address
   var port = server.address().port
   
   console.log("Example app listening at http://%s:%s", host, port)
})


MongoClient.connect('mongodb:http://ec2-54-202-24-50.us-west-2.compute.amazonaws.com/', (err, database) => {
	console.log(err)
})
