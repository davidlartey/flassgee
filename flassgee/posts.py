#Imports
import os
from werkzeug import cached_property
from sorted_dict import SortedDict

# Import Post class
from post import Post

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
