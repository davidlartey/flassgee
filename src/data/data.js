/**
 * ./src/data/data.js
 * 
 * Module to handle all data manipulation
 * 
 */
// Requirements
const fs = require("fs");

var AppEvents = require("./../core/eventEmitter.js");

// Collections and Models
var Pages = require("./page/collection.js"),
    Page = require("./page/model.js");

var Data = {

	pagesDir : "site/pages",
    
    path: null,

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

	},

	getPage : function(path) {
        
        path = this.parseUrl(path);
        
		var page = new Page({
					path: this.pagesDir,
					file: path
				});
		
        // console.log(page);
        return page.markdown();
        
	},
    
    parseUrl : function(url) {
        // Remove preceding /
        var path = url.replace("/", "", 1);
        console.log("Path: " + path);
        
        return path;
    },
    
    pageExists : function(path) {
        // Undefined
        var path = this.pagePath || "";
        
        // return Pages.isPage();
    }

};



AppEvents.on("respondToHttpRequest", function(req, res) {
    
    console.log("Handling Request: [" + req.method + "] " + req.url);
    
    var  pageData = Data.getPage(req.url);
    res.write(pageData);
    
});


// Export
module.exports = Data;