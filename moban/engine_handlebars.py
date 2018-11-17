import sys

from lml.plugin import PluginInfo

import moban.utils as utils
import moban.constants as constants
from moban import plugins
from pybars import Compiler


@PluginInfo(constants.TEMPLATE_ENGINE_EXTENSION, tags=["handlebars", "hbs"])
class EngineHandlebars(object):
    def __init__(self, template_dirs):
        self.template_dirs = template_dirs

    def get_template(self, template_file):
        actual_template_file = self.find_template_file(template_file)
        with open(actual_template_file, "r") as source:
            if sys.version_info[0] < 3:
                hbr_template = Compiler().compile(
                    unicode(source.read())  # noqa: F821
                )
            else:
                hbr_template = Compiler().compile(source.read())
        return plugins.Template(actual_template_file, hbr_template)

    def apply_template(self, template, data, output):
        rendered_content = "".join(template.template(data))
        rendered_content = utils.strip_off_trailing_new_lines(rendered_content)
        rendered_content = rendered_content.encode("utf-8")
        utils.write_file_out(
            output, rendered_content, strip=False, encode=False
        )
        utils.file_permissions_copy(template.abs_path, output)

    def find_template_file(self, template_file):
        return utils.get_template_path(self.template_dirs, template_file)
