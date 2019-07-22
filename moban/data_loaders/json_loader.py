import sys
import json

from moban import constants
from lml.plugin import PluginInfo

from fs import path, open_fs

PY2 = sys.version_info[0] == 2


@PluginInfo(constants.DATA_LOADER_EXTENSION, tags=["json"])
def open_json(file_name):
    """
    returns json contents as string
    """
    if PY2:
        if isinstance(file_name, unicode) is False:
            file_name = unicode(file_name)
    dir_name = path.dirname(file_name)
    the_file_name = path.basename(file_name)
    with open_fs(dir_name) as the_fs:
        with the_fs.open(the_file_name) as json_file:
            data = json.load(json_file)
            return data
