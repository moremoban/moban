import sys

from moban import constants
from lml.plugin import PluginInfo
from ruamel.yaml import YAML

from fs import path, open_fs

PY2 = sys.version_info[0] == 2


@PluginInfo(constants.DATA_LOADER_EXTENSION, tags=["yaml", "yml"])
def open_yaml(file_name):
    if PY2:
        if isinstance(file_name, unicode) is False:
            file_name = unicode(file_name)
    dir_name = path.dirname(file_name)
    the_file_name = path.basename(file_name)
    with open_fs(dir_name) as the_fs:
        with the_fs.open(the_file_name) as data_yaml:
            yaml = YAML(typ="rt")
            data = yaml.load(data_yaml)
            return data
