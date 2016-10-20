/**
 * App wide event emitter
 *
 */
// Requirements
const EventEmitter = require("events");

// Initialise
var appEvents = new EventEmitter();

// Return for everyone to use
module.exports = appEvents;