/**
 *
 *
 */

var Data = require("./data/data.js");
var express = require("express");

var app = express();

var server = function(Data) {

	// Register route
	app.get("/", function (req, res) {
		res.send("Hello world");
	});

	// Register param
	app.param("page", function (req, res, next, page) {
		next();

	});

	app.route("/:page", function(req, res, next, page) {

		// Get page's data
		pageData = Data.getPage(page);
		console.log(pageData);

	});

	app.listen(8000, function () {
		console.log("Started server");
	});

}

module.exports = server;