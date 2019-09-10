from moban import constants
from lml.plugin import PluginInfo
from ruamel.yaml import YAML
from moban.file_system import open_file


@PluginInfo(constants.DATA_LOADER_EXTENSION, tags=["yaml", "yml"])
def open_yaml(file_name):
    with open_file(file_name) as data_yaml:
        yaml = YAML(typ="rt")
        data = yaml.load(data_yaml)
        return data
