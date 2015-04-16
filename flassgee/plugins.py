

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
