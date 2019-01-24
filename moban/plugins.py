import os

from lml.loader import scan_plugins_regex
from lml.plugin import PluginManager

import moban.reporter as reporter
from moban import utils, constants, exceptions
from moban.strategy import Strategy
from moban.hashstore import HASH_STORE
from moban.data_loaders.manager import AnyDataLoader

BUILTIN_EXENSIONS = [
    "moban.jinja2.engine",
    "moban.data_loaders.yaml",
    "moban.data_loaders.json_loader",
]


class LibraryManager(PluginManager):
    def __init__(self):
        super(LibraryManager, self).__init__(constants.LIBRARY_EXTENSION)

    def resource_path_of(self, library_name):
        library = self.get_a_plugin(library_name)
        return library.resources_path


class BaseEngine(object):
    def __init__(
        self, template_dirs, context_dirs, engine_cls, engine_extensions=None
    ):
        # pypi-moban-pkg cannot be found if removed
        make_sure_all_pkg_are_loaded()
        template_dirs = list(expand_template_directories(template_dirs))
        verify_the_existence_of_directories(template_dirs)
        context_dirs = expand_template_directory(context_dirs)
        self.context = Context(context_dirs)
        self.template_dirs = template_dirs
        self.engine = engine_cls(self.template_dirs, engine_extensions)
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
        self.file_count = 1
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
            self.templated_count += 1

    def render_string_to_file(
        self, template_in_string, data_file, output_file
    ):
        self.file_count = 1
        template = self.engine.get_template_from_string(template_in_string)
        template_abs_path = template_in_string[:10] + "..."
        data = self.context.get_data(data_file)
        flag = self.apply_template(
            template_abs_path, template, data, output_file
        )
        if flag:
            reporter.report_templating(template_abs_path, output_file)
            self.templated_count += 1

    def apply_template(self, template_abs_path, template, data, output_file):
        rendered_content = self.engine.apply_template(
            template, data, output_file
        )
        rendered_content = utils.strip_off_trailing_new_lines(rendered_content)
        rendered_content = rendered_content.encode("utf-8")
        try:
            flag = HASH_STORE.is_file_changed(
                output_file, rendered_content, template_abs_path
            )
            if flag:
                utils.write_file_out(
                    output_file, rendered_content, strip=False, encode=False
                )
                utils.file_permissions_copy(template_abs_path, output_file)
            return flag
        except exceptions.FileNotFound:
            utils.write_file_out(
                output_file, rendered_content, strip=False, encode=False
            )
            return True

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
        self.extensions = {}

    def register_extensions(self, extensions):
        self.extensions.update(extensions)

    def get_engine(self, template_type, template_dirs, context_dirs):
        engine_cls = self.load_me_now(template_type)
        engine_extensions = self.extensions.get(template_type)
        return BaseEngine(
            template_dirs, context_dirs, engine_cls, engine_extensions
        )

    def all_types(self):
        return list(self.registry.keys())

    def raise_exception(self, key):
        raise exceptions.NoThirdPartyEngine(key)


LIBRARIES = LibraryManager()
ENGINES = EngineFactory()
LOADERS = AnyDataLoader()


def load_data(base_dir, file_name):
    abs_file_path = utils.search_file(base_dir, file_name)
    data = LOADERS.get_data(abs_file_path)
    if data is not None:
        parent_data = None
        if base_dir and constants.LABEL_OVERRIDES in data:
            parent_data = load_data(
                base_dir, data.pop(constants.LABEL_OVERRIDES)
            )
        if parent_data:
            return utils.merge(data, parent_data)
        else:
            return data
    else:
        return None


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
        try:
            data = load_data(self.context_dirs, file_name)
            utils.merge(data, self.__cached_environ_variables)
            return data
        except (IOError, exceptions.IncorrectDataInput) as exception:
            # If data file doesn't exist:
            # 1. Alert the user of their (potential) mistake
            # 2. Attempt to use environment vars as data
            reporter.report_warning_message(str(exception))
            reporter.report_using_env_vars()
            return self.__cached_environ_variables


def make_sure_all_pkg_are_loaded():
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
