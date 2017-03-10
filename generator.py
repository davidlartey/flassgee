#Core imports
import os
import sys
import collections

#Import Flask, render_template class from flask module
from flask import Flask, render_template, url_for, abort, request
from flask.ext.frozen import Freezer
from werkzeug import cached_property
from werkzeug.contrib.atom import AtomFeed
import markdown
import yaml

#constants
#Configuations
"""
class Configurations(object):
	
	DEBUG = True
	POST_FILES_DIRECTORY = 'posts'
	POST_FILE_EXTENSION = '.md'
	
	\"""Configurations class\"""
	def __init__(self):
		pass
"""

#Class to handle sorting
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

#Posts Class
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

	@property
	def latestPost(self) :
		posts = self.posts
		if (len(posts) > 0) :
			return posts[0]
		return False
	
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


#Post Class
class Post() :

	def __init__(self, path, root_dir = '') :
		self.url_path = os.path.splitext(path.strip('/'))[0]
		self.file_path = os.path.join(root_dir, path.strip('/'))
		self.published = False
		self._initialise_metadata()

	@cached_property
	def html(self) :
		with open(self.file_path, "r") as file_input :
			content = file_input.read().split("\n\n", 1)[1].decode('utf-8').strip()
		return markdown.markdown(content)

	def url(self, _external = False) :
		return url_for('post', path = self.url_path, _external = _external)

	# Custom private method.
	def _initialise_metadata(self) :
		content = ''
		with open(self.file_path, "r") as file_input :
			#Loop through each line of the file and after the first empty line add all other lines into the content var
			for line in file_input :
				if not line.decode('utf-8').strip() :
					break;

				content += line

		self.__dict__.update(yaml.load(content))


#Flask class instance
app = Flask(__name__)
#app.config.from_object(__name__) # Search for configurations in current module/file
#app.config.from_object(Configurations) # Use config class for configurations
import settings
app.config.from_object(settings) # Use the setting.py module/file with config values
#app.config.from_pyfile('settings.py') # Use the setting.py module/file with config values
#app.config.from_envvar('SETTINGS_FILE') # Set an env var SETTINGS_FILE with the absolute path of our settings file

# List of posts
posts = Posts(app, root_dir = app.config['POST_FILES_DIRECTORY'])


freezer = Freezer(app);

#Format dates 
@app.template_filter('date')
def format_date(value, format = '%B %d, %Y') :
	#Default format: %B %d, %Y
	return value.strftime(format)

# Register function as a Jinja filter
#app.jinja_env.filters['date'] = format_date

# This context processor was used to pass the function - or any other value - to the template
#@app.context_processor
#def inject_format_date() :
#	return { 'format_date' : format_date }
#

#Home Route
@app.route("/")
def index() :
	return render_template('index.html', post = posts.latestPost)

# Archives Home
@app.route("/all/")
def archives() :
	return render_template('archives.html', posts = posts.posts)

#Render a post
@app.route("/<path:path>/") # Submits a path string, path, to the post function
def post(path) :
	# import pdb
	# pdb.set_trace()
	#path = os.path.join(POST_FILES_DIRECTORY, path + POST_FILE_EXTENSION)
	#post = Post(path)
	#post = Post(path + POST_FILE_EXTENSION, root_dir = POST_FILES_DIRECTORY)
	post = posts.post_or_404(path)
	return render_template("post.html", post = post)

@app.route("/rss")
def atom_rss_feed() :
	feed = AtomFeed("Recent Articles", 
		feed_url = request.url,
		url = request.url_root
	)

	posts_list = posts.posts[:len(posts.posts)]
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
		app.config['DEBUG'] = True
		app.config['FREEZER_DESTINATION'] = "build"
		app.config['FREEZER_REMOVE_EXTRA_FILES'] = False
		app.config['FREEZER_DESTINATION_IGNORE'] = [ '.git', '.gitignore', 'CNAME' ]
		freezer.freeze()
	else :
		post_files = [post.file_path for post in posts.posts ]
		app.run(
			host = "172.18.12.227",
			port = 8000,
			debug = True,
			extra_files = post_files
		)
