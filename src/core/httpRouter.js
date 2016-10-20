/**
 * 
 *
 */
// Requirements
var AppEvents = require("./eventEmitter.js");


var HttpRouter = {
    
    // Request object
    req : null,
    
    // Response object
    res : null,
    
    /**
     * Bootstrap Routing
     * 
     * 
     */
    init : function(req, res) {
        // Store class attributes
        this.req = req;
        this.res = res;
        
        // Send the request to its specific handler
        this.handle();
    },
    

    /**
     * Handle Routing to parts of the application
     *
     *
     */
    handle : function () {
        
        /**
         * Use eventing for handling other request in the future
         * but for now all urls call for pages
        AppEvents.emit("handleRequest", [
            'url'
            'req' => this.req,
            'res' => this.res,
        ]);
        **/
        
        // Emit event for all other 
        AppEvents.emit("respondToHttpRequest", this.req, this.res);
        
    }
    
}

// Export
module.exports = function(req, res) {
    HttpRouter.init(req, res);
}