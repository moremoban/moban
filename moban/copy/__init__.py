from lml.plugin import PluginInfo

import codecs
import sys

from moban import utils
from moban import constants

PY2 = sys.version_info[0] == 2
if PY2:
    PermissionError = IOError


@PluginInfo(
    constants.TEMPLATE_ENGINE_EXTENSION,
    tags=[constants.TEMPLATE_COPY]
)
class Copier(object):
    def __init__(self, template_dirs, extensions=None):
        self.template_dirs = template_dirs

    def get_template(self, template_file):
        real_file_name = utils.find_file_in_template_dirs(
            template_file, self.template_dirs
        )
        with codecs.open(real_file_name, encoding="utf-8") as file_handle:
            return file_handle.read()

    def get_template_from_string(self, string):
        return string

    def apply_template(self, template, *_):
        return template
