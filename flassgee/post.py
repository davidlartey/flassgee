#Imports
import os
from flask import url_for
from werkzeug import cached_property
import markdown
import yaml


# Post Class
class Post() :

	def __init__(self, path, root_dir = '') :
		self.url_path = os.path.splitext(path.strip('/'))[0]
		self.file_path = os.path.join(root_dir, path.strip('/'))
		self.published = False
		self._initialise_metadata()

	@cached_property
	def html(self, charset = "utf-8") :
		with open(self.file_path, "r") as file_input :
			# Fetch content of file. Only consider after first blank line
			content = file_input.read().split("\n\n", 1)[1].strip()
			# Convert charset
			content = content.decode(charset)
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
