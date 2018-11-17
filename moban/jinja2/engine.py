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
        """
        Contruct a jinja2 template engine

        A list template directories will be given to your engine class

        :param list temp_dirs: a list of template directories
        """
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

    def get_template(self, template_file):
        """
        :param str template_file: the template file name that appeared in moban
                                  file. It could be a file name, or a relative
                                  file path with reference to template
                                  directories.
        :return: a jinja2 template

        For example:

        suppose your current working directory is: /User/moban-pro/ and your
        template folder list is: ['./my-template'], and the given template
        file equals to: 'templates/myfile.jj2', they as a group tells the
        template file exists at:
            '/User/moban-pro/my-template/templates/myfile.jj2'
        """
        template = self.jj2_environment.get_template(template_file)
        return template

    def apply_template(self, template, data, output):
        """
        It is not expected this function to write content to file system.
        Please just apply data inside the template and return utf-8 encoded
        content.

        :param template: a jinja2 template from :class:`.get_template`
        :param dict data: python data dictionary
        :param str output: output file name
        """
        template.globals["__target__"] = output
        template.globals["__template__"] = template.name
        rendered_content = template.render(**data)
        rendered_content = utils.strip_off_trailing_new_lines(rendered_content)
        rendered_content = rendered_content.encode("utf-8")
        return rendered_content
