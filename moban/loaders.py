from lml.plugin import PluginInfo

from moban import constants


class DataLoader(PluginInfo):
    def __init__(self):
        super(DataLoader, self).__init__(constants.DATA_LOADER_EXTENSION)
