import os

from lml.loader import scan_plugins_regex
from lml.plugin import PluginManager

import moban.reporter as reporter
from moban import utils, constants, exceptions
from moban.strategy import Strategy
from moban.hashstore import HASH_STORE


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

BUILTIN_EXENSIONS = [
    "moban.jinja2.filters.repr",
    "moban.jinja2.filters.github",
    "moban.jinja2.filters.text",
    "moban.jinja2.tests.files",
    "moban.jinja2.engine",
    "moban.engine_handlebars",
]


class LibraryManager(PluginManager):
    def __init__(self):
        super(LibraryManager, self).__init__(constants.LIBRARY_EXTENSION)

    def resource_path_of(self, library_name):
        library = self.get_a_plugin(library_name)
        return library.resources_path


class BaseEngine(object):
    def __init__(self, template_dirs, context_dirs, engine_cls):
        refresh_plugins()
        template_dirs = list(expand_template_directories(template_dirs))
        verify_the_existence_of_directories(template_dirs)
        context_dirs = expand_template_directory(context_dirs)
        self.context = Context(context_dirs)
        self.template_dirs = template_dirs
        self.engine = engine_cls(self.template_dirs)
        self.engine_cls = engine_cls
        self.templated_count = 0
        self.file_count = 0

    def report(self):
        if self.templated_count == 0:
            reporter.report_no_action()
        elif self.templated_count == self.file_count:
            reporter.report_full_run(self.file_count)
        else:
            reporter.report_partial_run(self.templated_count, self.file_count)

    def number_of_templated_files(self):
        return self.templated_count

    def render_to_file(self, template_file, data_file, output_file):
        data = self.context.get_data(data_file)
        template = self.engine.get_template(template_file)
        template_abs_path = utils.get_template_path(
            self.template_dirs, template_file
        )
        flag = self.apply_template(
            template_abs_path, template, data, output_file
        )
        if flag:
            reporter.report_templating(template_file, output_file)

    def apply_template(self, template_abs_path, template, data, output_file):
        rendered_content = self.engine.apply_template(
            template, data, output_file
        )
        flag = HASH_STORE.is_file_changed(
            output_file, rendered_content, template_abs_path
        )
        if flag:
            utils.write_file_out(
                output_file, rendered_content, strip=False, encode=False
            )
            utils.file_permissions_copy(template_abs_path, output_file)
        return flag

    def render_to_files(self, array_of_param_tuple):
        sta = Strategy(array_of_param_tuple)
        sta.process()
        choice = sta.what_to_do()
        if choice == Strategy.DATA_FIRST:
            self._render_with_finding_data_first(sta.data_file_index)
        else:
            self._render_with_finding_template_first(sta.template_file_index)

    def _render_with_finding_template_first(self, template_file_index):
        for (template_file, data_output_pairs) in template_file_index.items():
            template = self.engine.get_template(template_file)
            template_abs_path = utils.get_template_path(
                self.template_dirs, template_file
            )
            for (data_file, output) in data_output_pairs:
                data = self.context.get_data(data_file)
                flag = self.apply_template(
                    template_abs_path, template, data, output
                )
                if flag:
                    reporter.report_templating(template_file, output)
                    self.templated_count += 1
                self.file_count += 1

    def _render_with_finding_data_first(self, data_file_index):
        for (data_file, template_output_pairs) in data_file_index.items():
            data = self.context.get_data(data_file)
            for (template_file, output) in template_output_pairs:
                template = self.engine.get_template(template_file)
                template_abs_path = utils.get_template_path(
                    self.template_dirs, template_file
                )
                flag = self.apply_template(
                    template_abs_path, template, data, output
                )
                if flag:
                    reporter.report_templating(template_file, output)
                    self.templated_count += 1
                self.file_count += 1


class EngineFactory(PluginManager):
    def __init__(self):
        super(EngineFactory, self).__init__(
            constants.TEMPLATE_ENGINE_EXTENSION
        )

    def get_engine(self, template_type, template_dirs, context_dirs):
        engine_cls = self.load_me_now(template_type)
        return BaseEngine(template_dirs, context_dirs, engine_cls)

    def all_types(self):
        return list(self.registry.keys())

    def raise_exception(self, key):
        raise exceptions.NoThirdPartyEngine(key)


LIBRARIES = LibraryManager()
ENGINES = EngineFactory()


def expand_template_directories(dirs):
    if not isinstance(dirs, list):
        dirs = [dirs]

    for directory in dirs:
        yield expand_template_directory(directory)


def expand_template_directory(directory):
    translated_directory = None
    if ":" in directory:
        library_or_repo_name, relative_path = directory.split(":")
        potential_repo_path = os.path.join(
            utils.get_moban_home(), library_or_repo_name
        )
        if os.path.exists(potential_repo_path):
            # expand repo template path
            if relative_path:
                translated_directory = os.path.join(
                    potential_repo_path, relative_path
                )
            else:
                translated_directory = potential_repo_path
        else:
            # expand pypi template path
            library_path = LIBRARIES.resource_path_of(library_or_repo_name)
            if relative_path:
                translated_directory = os.path.join(
                    library_path, relative_path
                )
            else:
                translated_directory = library_path
    else:
        # local template path
        translated_directory = os.path.abspath(directory)
    return translated_directory


class Context(object):
    def __init__(self, context_dirs):
        verify_the_existence_of_directories(context_dirs)
        self.context_dirs = context_dirs
        self.__cached_environ_variables = dict(
            (key, os.environ[key]) for key in os.environ
        )

    def get_data(self, file_name):
        file_extension = os.path.splitext(file_name)[1]
        if file_extension == ".json":
            data = utils.open_json(self.context_dirs, file_name)
        elif file_extension in [".yml", ".yaml"]:
            data = utils.open_yaml(self.context_dirs, file_name)
            utils.merge(data, self.__cached_environ_variables)
        else:
            raise exceptions.IncorrectDataInput
        return data


def refresh_plugins():
    scan_plugins_regex(constants.MOBAN_ALL, "moban", None, BUILTIN_EXENSIONS)


def verify_the_existence_of_directories(dirs):
    if not isinstance(dirs, list):
        dirs = [dirs]

    for directory in dirs:
        if os.path.exists(directory):
            continue
        should_I_ignore = (
            constants.DEFAULT_CONFIGURATION_DIRNAME in directory
            or constants.DEFAULT_TEMPLATE_DIRNAME in directory
        )
        if should_I_ignore:
            # ignore
            pass
        else:
            raise exceptions.DirectoryNotFound(
                constants.MESSAGE_DIR_NOT_EXIST % os.path.abspath(directory)
            )
