
"""
settings.py
Site: DavidLartey.com
"""
class SiteSettings() :

	def __init__(self) :
		pass

	def test_run() :
		print "in here"

	#POST_FILES_DIRECTORY = 'posts'
	#POST_FILE_EXTENSION = '.md'
	#FREEZER_BASE_URL = 'http://davidlartey.com'

# """
# old
DEBUG = True
POST_FILES_DIRECTORY = 'posts'
POST_FILE_EXTENSION = '.md'

FREEZER_BASE_URL = 'http://davidlartey.com'
FREEZER_DESTINATION = ''
FREEZER_DESTINATION_IGNORE = ['.git*', 'CNAME'] # Ignore the files in the list

POSTS_URL_PREFIX = "blog/"  #If not empty (no prefix, just add post url to base_url/) end with a backslash
POSTS_ON_HOME_PAGE = 1; #The number of posts to show on the home page

SITE_TITLE = "David Lartey"
SITE_DESCRIPTION = "#LifeIsBeautiful"
SITE_DESCRIPTION_URL = "blog/about"
# SITE_SPECIAL_PAGES = ['']
# """