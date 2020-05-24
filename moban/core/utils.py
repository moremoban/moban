import os
import re
import sys
import logging

from lml.utils import do_import

from moban import constants
from moban.externals import file_system

LOG = logging.getLogger(__name__)


def verify_the_existence_of_directories(dirs):
    if not isinstance(dirs, list):
        dirs = [dirs]

    dirs = [
        directory
        for directory in dirs
        if not (
            constants.DEFAULT_CONFIGURATION_DIRNAME in directory
            or constants.DEFAULT_TEMPLATE_DIRNAME in directory
        )
    ]
    if file_system.exists(constants.DEFAULT_CONFIGURATION_DIRNAME):
        dirs.append(constants.DEFAULT_CONFIGURATION_DIRNAME)

    if file_system.exists(constants.DEFAULT_TEMPLATE_DIRNAME):
        dirs.append(constants.DEFAULT_TEMPLATE_DIRNAME)
    return dirs


def handle_plugin_dirs(plugin_dirs):
    if plugin_dirs is None:
        return
    LOG.info("handling plugin dirs {}".format(",".join(plugin_dirs)))
    for plugin_dir in plugin_dirs:
        plugin_path = os.path.normcase(
            os.path.dirname(os.path.abspath(plugin_dir))
        )
        if plugin_path not in sys.path:
            sys.path.append(plugin_path)
        pysearchre = re.compile(".py$", re.IGNORECASE)
        pluginfiles = filter(pysearchre.search, os.listdir(plugin_dir))
        plugins = list(map(lambda fp: os.path.splitext(fp)[0], pluginfiles))
        for plugin in plugins:
            plugin_module = os.path.basename(plugin_dir) + "." + plugin
            do_import(plugin_module)
