import json

from moban import constants
from lml.plugin import PluginInfo


@PluginInfo(constants.DATA_LOADER_EXTENSION, tags=["json"])
def open_json(file_name):
    """
    returns json contents as string
    """
    with open(file_name, "r") as json_data:
        data = json.load(json_data)
        return data
