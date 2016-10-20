/**
 * Main application Kernel
 * Currently HTTP requests
 *
 */
var HttpRouter = require("./HttpRouter");

var HttpRequestHandler = {
    
    /**
     * Handle HTTP Requests
     *
     * @param req
     * @param res
     * @return void
     */
    handle : function(req, res) {
        
        // Pass request through router
        HttpRouter(req, res);
        
        // Respond
        res.end();
    }
    
};

// Export
module.exports = HttpRequestHandler;