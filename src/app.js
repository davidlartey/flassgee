/**
 * ./src/app.js
 *
 */
// Requirements
const http = require("http");


const express = require("express");


var Data = require("./data/data.js"),
	server = require("./server.js");

var App = {

	/**
	 *
	 */
	init : function() {
		console.log("Initialising application");

		server();

		this.run();
	},


	serve : function() {

		server.listen(8000, function () {
			console.log("Started server on port 8000");
		});

	},

	/**
	 * Run Generator
	 */
	run : function() {
		// 1. Fetch list of markdown posts available
		var pages = Data.getPages();

		// 2. Format markdown
		// 3. Render templates
		// 4. Save rendered content
	}
};

module.exports = function() {
	App.init();
}