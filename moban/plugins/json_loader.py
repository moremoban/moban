import json

from lml.plugin import PluginInfo

from moban import constants
from moban.externals.file_system import open_file


@PluginInfo(constants.DATA_LOADER_EXTENSION, tags=["json"])
def open_json(file_name):
    """
    returns json contents as string
    """
    with open_file(file_name) as json_file:
        data = json.load(json_file)
        return data
