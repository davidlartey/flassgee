try :
	from setuptools import setup

except ImportError :
	from distutils.core import setup


config = {
	'name' : 'FlaSSGee',
	'description' : "Flask based Static Site Generator",
	'version' : "0.1",
	'url' : 'https://github.com/davidlartey/flassgee',
	'download_url' : "https://github.com/davidlartey/flassgee",
	'author' : "David Lartey",
	'author_email' : "me@davidlartey.com",
	'install_requires' : ['nose'],
	'packages' : ['NAME'],
	'scripts' : []
}

setup(**config)

