from jinja2 import Environment, FileSystemLoader
from lml.plugin import PluginInfo

import moban.utils as utils
import moban.constants as constants
from moban import plugins


@PluginInfo(
    constants.TEMPLATE_ENGINE_EXTENSION, tags=["jinja2", "jinja", "jj2", "j2"]
)
class Engine(object):
    def __init__(self, template_dirs):
        self.template_dirs = template_dirs
        template_loader = FileSystemLoader(template_dirs)
        self.jj2_environment = Environment(
            loader=template_loader,
            keep_trailing_newline=True,
            trim_blocks=True,
            lstrip_blocks=True,
        )
        for filter_name, filter_function in plugins.FILTERS.get_all():
            self.jj2_environment.filters[filter_name] = filter_function

        for test_name, test_function in plugins.TESTS.get_all():
            self.jj2_environment.tests[test_name] = test_function

        for global_name, dict_obj in plugins.GLOBALS.get_all():
            self.jj2_environment.globals[global_name] = dict_obj

    def apply_template(self, template, data, output):
        template.globals["__target__"] = output
        template.globals["__template__"] = template.name
        rendered_content = template.render(**data)
        rendered_content = utils.strip_off_trailing_new_lines(rendered_content)
        rendered_content = rendered_content.encode("utf-8")
        return rendered_content

    def get_template(self, template_file):
        template = self.jj2_environment.get_template(template_file)
        return template
