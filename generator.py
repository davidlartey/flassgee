#Core imports
import os , sys, inspect, collections

#Import Flask, render_template class from flask module
from flask import Flask, render_template, url_for, abort, request, send_from_directory
from flask.ext.frozen import Freezer
from werkzeug.contrib.atom import AtomFeed
import markdown
import yaml
import jinja2

# Classes Imports
from flassgee.posts import Posts
from flassgee.post import Post

# Flask instance
app = Flask(__name__)

# Use the setting.py module/file with config values
import settings
app.config.from_object(settings)

"""
Flassgee custom flask functions
"""
# custom Jinja templates loader
flassgeeJinjaLoader = jinja2.ChoiceLoader([
	app.jinja_loader,
	jinja2.FileSystemLoader('sites/' + app.config['SITE'] + '/templates')
]);
# set flask to use flassgeeJinjaLoader
app.jinja_loader = flassgeeJinjaLoader

# Custom static files loader
@app.route('/fsf/<path:filename>')
def flassgee_static_files(filename) :
	# return the static files in that site's directory
	return send_from_directory('sites/' + app.config['SITE'] + '/static', filename)

# List of posts
posts = Posts(app, root_dir = app.config['POST_FILES_DIRECTORY'])

# Freezer instance
freezer = Freezer(app);

# Format dates 
# Register date werkzeug filter
@app.template_filter('date')
# Default format: %B %d, %Y
def format_date(value, format = '%B %d, %Y') :
	return value.strftime(format)

#Home Route
@app.route("/")
def index() :
	# Render index.html template
	home_page_posts = posts.posts

	if app.config['POSTS_ON_HOME_PAGE'] :
		home_page_posts = home_page_posts[:app.config['POSTS_ON_HOME_PAGE']]
	print home_page_posts
	return render_template('index.html', app_config = app.config, posts = home_page_posts)

"""
# Test plugins route
@app.route("/plugins")
def plugins() :
	fsg_plugins = Plugins(app)
	return fsg_plugins.plugins
"""

#Render a post
@app.route("/" + app.config['POSTS_URL_PREFIX'] + "<path:path>/") # Submits a path string, path, to the post function
def post(path) :
	# Render a single post or 404 page
	return render_template("post.html", app_config = app.config, post = posts.post_or_404(path))

@app.route("/rss")
def atom_rss_feed() :
	feed = AtomFeed("Recent Articles", 
		feed_url = request.url,
		url = request.url_root
	)

	posts_list = posts.posts[:10]
	#articles = Article.query.order_by(Article.pub_date.desc()).limit(15).all()

	title = lambda p: '%s : %s' % (p.title, p.subtitle) if hasattr(p, 'subtitle') else p.title

	for post in posts_list :
		feed.add(
			title(post),
			unicode(post.html),
			content_type = "html",
			author = 'David Lartey',
			url = post.url(_external = True),
			updated = post.date,
			published = post.date
		)

	return feed.get_response()

"""
Get previous, current, next items from a list.
"""
from itertools import tee, islice, chain, izip
def get_previous_and_next_items() :
	print sys.argv
	previous, current, next = tee(sys.argv, 3)
	previous = chain([None], 1)
	next = chain(islice(next, 1, None), [None])
	# return
	return izip(previous, current, next)

#Run app
if __name__ == '__main__' :

	# Only freeze site when the build command is sent
	if len(sys.argv) > 1 and sys.argv[1] == "build" :
		# python generator.py build
		app.config['DEBUG'] = False

		if sys.argv[2] :
			# command: python generator.py build /path/to/save/build/files
			freezer_destination = sys.argv[2]
			app.config['FREEZER_DESTINATION'] = freezer_destination

		freezer.freeze()

	elif len(sys.argv) > 1 :
		"""
		args = sys.argv
		for previous_argv, argv, next_argv in get_previous_and_next_items() :
			if argv == '-s' or argv == '--site' :
				print next_argv
		"""

	else :
		# python generator.py
		post_files = [post.file_path for post in posts.posts ]
		app.run(
			port = 8002,
			#debug = True,
			extra_files = post_files
		)
