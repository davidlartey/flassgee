/**
 * ./src/data/data.js
 * 
 * Module to handle all data manipulation
 * 
 */
// Requirements
const fs = require("fs");

// Collections and Models
var Pages = require("./page/collection.js");

var Data = {

	pagesDir : "site/pages",

	/**
	 *
	 */
	getPages : function() {
		var self = this;

		// Read pages directory
		var files = fs.readdirSync(this.pagesDir);

		// List files
		var pages = Pages({
			path: self.pagesDir,
			files: files
		});

	}

};

// Export
module.exports = Data;