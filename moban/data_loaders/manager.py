import os

from lml.plugin import PluginManager

from moban import constants


class AnyDataLoader(PluginManager):
    def __init__(self):
        super(AnyDataLoader, self).__init__(constants.DATA_LOADER_EXTENSION)

    def get_data(self, file_name):
        file_extension = os.path.splitext(file_name)[1]
        file_type = file_extension
        if file_extension.startswith("."):
            file_type = file_type[1:]

        try:
            loader_function = self.load_me_now(file_type)
        except Exception:
            loader_function = self.load_me_now(constants.DEFAULT_DATA_TYPE)
        return loader_function(file_name)
