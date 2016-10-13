/**
 *
 *
 */
var Model = require("./model.js");


var Collection = {

	models : [],

	/**
	 * Initialise collections with models
	 */
	init : function(options) {

		if (options.files) {
			for (var i = 0; i < options.files.length; i++) {
				var model = Model({
					path: options.path,
					file: options.files[i]
				});

				console.log(model.markdown());

				this.models.push(model);
			}
		}

		// Return
		return this;
	}


};

module.exports = function(options) {
	return Collection.init(options);
}