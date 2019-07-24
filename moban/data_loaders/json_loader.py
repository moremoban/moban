import json

from moban import constants
from lml.plugin import PluginInfo
from moban.file_system import open_fs


@PluginInfo(constants.DATA_LOADER_EXTENSION, tags=["json"])
def open_json(file_name):
    """
    returns json contents as string
    """
    with open_fs(file_name) as json_file:
        data = json.load(json_file)
        return data
