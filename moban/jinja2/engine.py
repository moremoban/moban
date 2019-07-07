import re
from importlib import import_module

from moban import constants, exceptions
from jinja2 import Template, Environment, FileSystemLoader
from lml.loader import scan_plugins_regex
from lml.plugin import PluginInfo, PluginManager
from jinja2.exceptions import TemplateNotFound

JINJA2_LIBRARIES = "^moban_jinja2_.+$"
JINJA2_EXENSIONS = [
    "moban.jinja2.filters.repr",
    "moban.jinja2.filters.github",
    "moban.jinja2.filters.text",
    "moban.jinja2.tests.files",
]
JINJA2_THIRD_PARTY_EXTENSIONS = ["jinja2.ext.do", "jinja2.ext.loopcontrols"]


class PluginMixin:
    def get_all(self):
        for name in self.registry.keys():
            # only the first matching one is returned
            the_filter = self.load_me_now(name)
            yield (name, the_filter)


class JinjaFilterManager(PluginManager, PluginMixin):
    def __init__(self):
        super(JinjaFilterManager, self).__init__(
            constants.JINJA_FILTER_EXTENSION
        )


class JinjaTestManager(PluginManager, PluginMixin):
    def __init__(self):
        super(JinjaTestManager, self).__init__(constants.JINJA_TEST_EXTENSION)


class JinjaGlobalsManager(PluginManager, PluginMixin):
    def __init__(self):
        super(JinjaGlobalsManager, self).__init__(
            constants.JINJA_GLOBALS_EXTENSION
        )


FILTERS = JinjaFilterManager()
TESTS = JinjaTestManager()
GLOBALS = JinjaGlobalsManager()


@PluginInfo(
    constants.TEMPLATE_ENGINE_EXTENSION, tags=["jinja2", "jinja", "jj2", "j2"]
)
class Engine(object):
    def __init__(self, template_dirs, options=None):
        """
        Contruct a jinja2 template engine

        A list template directories will be given to your engine class

        :param list temp_dirs: a list of template directories
        :param dict options: a dictionary containing environmental parameters
        """
        load_jinja2_extensions()
        self.template_dirs = template_dirs
        template_loader = FileSystemLoader(template_dirs)
        env_params = dict(
            loader=template_loader,
            keep_trailing_newline=True,
            trim_blocks=True,
            lstrip_blocks=True,
            extensions=[
                extension for extension in JINJA2_THIRD_PARTY_EXTENSIONS
            ],  # get a copy of this global variable
        )
        if options:
            if "extensions" in options:
                extensions = options.pop("extensions")
                if is_extension_list_valid(extensions):
                    # because it is modified here
                    env_params["extensions"] += extensions
                    import_module_of_extension(extensions)

            env_params.update(options)
        self.jj2_environment = Environment(**env_params)
        for filter_name, filter_function in FILTERS.get_all():
            self.jj2_environment.filters[filter_name] = filter_function

        for test_name, test_function in TESTS.get_all():
            self.jj2_environment.tests[test_name] = test_function

        for global_name, dict_obj in GLOBALS.get_all():
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
        try:
            template = self.jj2_environment.get_template(template_file)
        except TemplateNotFound:
            raise exceptions.FileNotFound("%s does not exist" % template_file)
        return template

    def get_template_from_string(self, string):
        return Template(string)

    def apply_template(self, template, data, output):
        """
        It is not expected this function to write content to file system.
        Please just apply data inside the template and return utf-8
        content.

        :param template: a jinja2 template from :class:`.get_template`
        :param dict data: python data dictionary
        :param str output: output file name
        """
        template.globals["__target__"] = output
        template.globals["__template__"] = template.name
        rendered_content = template.render(**data)
        rendered_content = strip_off_trailing_new_lines(rendered_content)
        return rendered_content


def load_jinja2_extensions():
    scan_plugins_regex(JINJA2_LIBRARIES, "moban", None, JINJA2_EXENSIONS)


def is_extension_list_valid(extensions):
    return (
        extensions is not None
        and isinstance(extensions, list)
        and len(extensions) > 0
    )


def import_module_of_extension(extensions):
    modules = set()
    if extensions:
        for extension in extensions:
            modules.add(extension.split(".")[0])
    for module in modules:
        import_module(module)


def strip_off_trailing_new_lines(content):
    return re.sub(r"(\n\s+)+$", r"\n", content)
