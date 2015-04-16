DEBUG = True
PLUGINS_DIRECTORY = 'plugins'

POST_FILES_DIRECTORY = 'posts--'
POST_FILE_EXTENSION = '.md'

FREEZER_BASE_URL = 'http://flassgee.github.io'
FREEZER_DESTINATION = ''
FREEZER_DESTINATION_IGNORE = ['.git*', 'CNAME'] # Ignore the files in the list

POSTS_URL_PREFIX = "blog/"  #If not empty (no prefix, just add post url to base_url/) end with a backslash
POSTS_ON_HOME_PAGE = 1; #The number of posts to show on the home page

SITE_TITLE = "flassgee"
SITE_DESCRIPTION = "FLAsk (based) Static Site Generator"
SITE_DESCRIPTION_URL = "blog/about"
# SITE_SPECIAL_PAGES = ['']



SITES = ['example-site', 'davidlartey-com']
# SITE = 'example-site'
SITE = 'davidlartey-com'

if SITE :

	import sys
	# Import site specific setting files
	sys.path.insert(0, 'sites/' + SITE);
	import site_settings

	# Update globals
	globals().update(vars(sys.modules['site_settings']))

	print POST_FILES_DIRECTORY


# print POST_FILES_DIRECTORY