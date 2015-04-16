#Core imports
import os , sys, inspect, collections

#Import Flask, render_template class from flask module
from flask import Flask, render_template, url_for, abort, request
from flask.ext.frozen import Freezer
from werkzeug import cached_property
from werkzeug.contrib.atom import AtomFeed
import markdown
import yaml


# Class to handle sorting of posts by date
class SortedDict(collections.MutableMapping) :

	def __init__(self, items = None, key = None, reverse = False) :
		self._items = {}
		self._keys = []
		if key :
			self._key_fn = lambda k: key(self._items[k])
		else :
			self._key_fn = lambda k: self._items[k]

		self._reverse = reverse

		if items is not None :
			self.update(items)


	def __getitem__(self, key) :
		return self._items[key]

	def __setitem__(self, key, value) :
		self._items[key] = value
		if key not in self._keys :
			self._keys.append(key)
			self._keys.sort(key = self._key_fn, reverse = self._reverse)

	def __delitem__(self, key) :
		self._items.pop(key)
		self._keys.remove(key)

	def __len__(self) :
		return len(self._keys)

	def __iter__(self) :
		for key in self._keys :
			yield key

	def __repr__(self) :
		return '%s(%s)' % (self.__class__.__name__, self._items)


# Plugins class
class Plugins() :
	
	def __init__(self, app, plugins_dir = 'plugins') :
		self._app = app
		self.plugins_dir = plugins_dir
		# self._initialise_plugins()

	# List of plugins
	@property
	def plugins(self) :
		# list of plugins
		plugins = []
		plugins_dir_subdirs = os.listdir(self.plugins_dir)
		for plugin_dir in plugins_dir_subdirs :
			default_plugin_file_path = self.plugins_dir + '/' + plugin_dir + '/' + plugin_dir + ".py"
			# Remove directories without proper plugin file name from list of plugins_dir_subdirs
			if os.access(default_plugin_file_path, os.F_OK) :
				plugin = Plugin(plugin_file = default_plugin_file_path)
				plugins.append(plugin)
			else :
				plugins_dir_subdirs.remove(plugin_dir)
				# del plugins_dir_subdirs[plugin]
		
		print plugins_dir_subdirs

		count = 0
		for plugin in plugins :
			count += 1
			print count, plugin.name


class Plugin() :
	
	# Attributes
	name = 'Plugin'
	version = '0.01',
	status = 'disabled'

	def __init__(self, plugin_file) :
		self.plugin_file_path = plugin_file
		# Import plugin file
		plugin_file_import = os.path.splitext(self.plugin_file_path.strip('/'))[0]
		app_folder = os.path.realpath(os.path.abspath(os.path.split(inspect.getfile(inspect.currentframe()))[0]))
		if app_folder not in sys.path :
			sys.path.insert(0, app_folder)

		app_subfolder
		# import "%s" % plugin_file_import
		# plugin_file_import.test()
		# import 
		# Get plugin directory from default plugin file path
		#self.
		#print self.plugin_file_path.split('/')

# Posts Class
class Posts() :
	
	def __init__(self, app, root_dir = '', file_extension = None) :
		self.root_dir = root_dir
		self.file_extension = file_extension if file_extension is not None else app.config['POST_FILE_EXTENSION']
		self._app = app
		self._cache = SortedDict(key = lambda p: p.date, reverse = True)
		self._initialise_cache()

	@property
	def posts(self):
		if self._app.debug :
			return self._cache.values()
		else :
			return [post for post in self._cache.values() if post.published]
	
	def post_or_404 (self, path) :
		"""
		"""
		try :
			return self._cache[path]
		except KeyError :
			abort(404)

	def _initialise_cache(self) :
		"""
		Walks - loops - through the root directory and adds a list of all posts and their path to the _initialise_cache
		method of the Posts class.
		"""
		for (root, dirpaths, filepaths) in os.walk(self.root_dir) :
			for filepath in filepaths :
				filename, ext = os.path.splitext(filepath)
				if ext == self.file_extension :
					path = os.path.join(root, filepath).replace(self.root_dir, '')
					post = Post(path, root_dir = self.root_dir)
					self._cache[post.url_path] = post


# Post Class
class Post() :

	def __init__(self, path, root_dir = '') :
		self.url_path = os.path.splitext(path.strip('/'))[0]
		self.file_path = os.path.join(root_dir, path.strip('/'))
		self.published = False
		self._initialise_metadata()

	@cached_property
	def html(self) :
		with open(self.file_path, "r") as file_input :
			content = file_input.read().split("\n\n", 1)[1].strip()
		return markdown.markdown(content, extensions = ['codehilite'])

	def url(self, _external = False) :
		return url_for('post', path = self.url_path, _external = _external)

	# Custom private method.
	def _initialise_metadata(self) :
		content = ''
		with open(self.file_path, "r") as file_input :
			#Loop through each line of the file and after the first empty line add all other lines into the content var
			for line in file_input :
				if not line.strip() :
					break;

				content += line

		self.__dict__.update(yaml.load(content))


# Flask instance
app = Flask(__name__)

# Use the setting.py module/file with config values
import settings
app.config.from_object(settings)

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
	return render_template('index.html', posts = posts.posts)

# Test plugins route
@app.route("/plugins")
def plugins() :
	fsg_plugins = Plugins(app)
	return fsg_plugins.plugins

#Render a post
@app.route("/blog/<path:path>/") # Submits a path string, path, to the post function
def post(path) :
	post = posts.post_or_404(path)
	return render_template("post.html", post = post)

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

#Run app
if __name__ == '__main__' :
	# Only freeze site when the build command is sent
	if len(sys.argv) > 1 and sys.argv[1] == "build" :
		app.config['DEBUG'] = False
		freezer.freeze()
	else :
		post_files = [post.file_path for post in posts.posts ]
		app.run(
			port = 8000,
			#debug = True,
			extra_files = post_files
		)
