from moban import constants
from lml.plugin import PluginManager


class LibraryManager(PluginManager):
    def __init__(self):
        super(LibraryManager, self).__init__(constants.LIBRARY_EXTENSION)

    def resource_path_of(self, library_name):
        library = self.get_a_plugin(library_name)
        return library.resources_path


LIBRARIES = LibraryManager()
