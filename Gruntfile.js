/**
 * Tasks
 *  - matchdep
 * 	- grunt-contrib-clean
 * 	- grunt-contrib-watch
 */
module.exports = function (grunt) {
	grunt.initConfig({
		pkg: grunt.file.readJSON("package.json"),

		// Clean
        clean : {
            build : 'build/*' // Clean build dir
        },

        // Watch
        watch : {
            grunt : {
                files : ['Gruntfile.js'],
                tasks : ["clean:build", "sass", "browserify:dev" ]
            },
            js : {
                files : [ '*.js', 'src/**/*.js', '!build/*.js'],
                tasks : [ "clean:build" ]
            }
        }
	});

    // Load all grunt contribs installed
    require('matchdep').filterDev('grunt-*').forEach(grunt.loadNpmTasks);

    // Register default task
	grunt.registerTask("default", [ "watch" ]);
};
