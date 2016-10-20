/**
 * ./src/app.js
 *
 */
// Requirements
var Server = require("./server.js"),
    Data = require("./data/data.js");

var App = {

	/**
	 *
	 */
	init : function() {
		console.log("Initialising application");

		Server();

		// this.run();
	},


	serve : function() {

		server.listen(8000, function () {
			console.log("Started server on port 8000");
		});
        
        server.on("request", function(req, res) {
            console.log(req.url);
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