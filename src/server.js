/**
 *
 *
 */
// Requirements
const http = require("http");

// HttpKernel
var HttpRequestHandler = require("./core/kernel.js");

var Server = function() {
    
    var server = http.createServer(function(req, res) {
        HttpRequestHandler.handle(req, res);
    });
    
    // 

    // Listen
	server.listen(8000, function() {
        console.log("Listening on port 8000");
    });

}

module.exports = Server;