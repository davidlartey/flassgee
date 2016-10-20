/**
 * ./src/data/page/model.js
 *
 * A Page
 *
 */
const fs = require("fs"),
    path = require("path");

var markdown = require("markdown").markdown;

var Page = {

	path : null,

	file : null,



	/**
	 * Initialiser
	 */
	init : function(options) {
		this.path = options.path;
		this.file = options.file;

		// Return 
		return this;
	},


	/**
	 * Read, format and return markdown 
	 */
	markdown : function() {
		// Get full path
		var fullPath = String(path.join(this.path, this.file) + ".md");

		// Read markdown file
		var data = fs.readFileSync(fullPath, 'utf8');

		// Return html
		return markdown.toHTML(data);
	}

};

// Export
module.exports = function(options) {
	return Page.init(options);
};