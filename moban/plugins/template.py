import os
import sys
import logging

from moban import repo, utils, reporter, constants, exceptions
from lml.plugin import PluginManager
from moban.hashstore import HASH_STORE
from moban.plugins.context import Context
from moban.plugins.library import LIBRARIES
from moban.plugins.strategy import Strategy

log = logging.getLogger(__name__)
PY3_ABOVE = sys.version_info[0] > 2


class MobanFactory(PluginManager):
    def __init__(self):
        super(MobanFactory, self).__init__(constants.TEMPLATE_ENGINE_EXTENSION)
        self.extensions = {}
        self.options_registry = {}

    def register_extensions(self, extensions):
        self.extensions.update(extensions)

    def register_options(self, template_types):
        # need the value of 'template_types'
        # see test_get_user_defined_engine for help
        self.options_registry.update(template_types)

    def get_engine(self, template_type, template_dirs, context_dirs):
        if template_type in self.options_registry:
            custom_engine_spec = self.options_registry[template_type]
            engine_cls = self.load_me_now(
                custom_engine_spec[constants.TEMPLATE_TYPES_BASE_TYPE]
            )
            options = custom_engine_spec[constants.TEMPLATE_TYPES_OPTIONS]
        else:
            engine_cls = self.load_me_now(template_type)
            engine_extensions = self.extensions.get(template_type)
            options = dict(extensions=engine_extensions)
        engine = engine_cls(template_dirs, options)
        return MobanEngine(template_dirs, context_dirs, engine)

    def get_primary_key(self, template_type):
        for key, item in self.options_registry.items():
            if template_type in item[constants.TEMPLATE_TYPES_FILE_EXTENSIONS]:
                return key

        return super(MobanFactory, self).get_primary_key(template_type)

    def all_types(self):
        return list(self.registry.keys()) + list(self.options_registry.keys())

    def raise_exception(self, key):
        raise exceptions.NoThirdPartyEngine(key)


class MobanEngine(object):
    def __init__(self, template_dirs, context_dirs, engine):
        template_dirs = list(expand_template_directories(template_dirs))
        utils.verify_the_existence_of_directories(template_dirs)
        context_dirs = expand_template_directory(context_dirs)
        self.context = Context(context_dirs)
        self.template_dirs = template_dirs
        self.engine = engine
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
        if PY3_ABOVE:
            if not isinstance(rendered_content, bytes):
                rendered_content = rendered_content.encode("utf-8")

        try:
            flag = HASH_STORE.is_file_changed(
                output_file, rendered_content, template_abs_path
            )
            if flag:
                utils.write_file_out(output_file, rendered_content)
                utils.file_permissions_copy(template_abs_path, output_file)
            return flag
        except exceptions.FileNotFound:
            utils.write_file_out(output_file, rendered_content)
            return True

    def render_to_files(self, array_of_template_targets):
        sta = Strategy(array_of_template_targets)
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


def expand_template_directories(dirs):
    log.debug("Expanding %s..." % dirs)
    if not isinstance(dirs, list):
        dirs = [dirs]

    for directory in dirs:
        yield expand_template_directory(directory)


def expand_template_directory(directory):
    log.debug("Expanding %s..." % directory)
    translated_directory = None
    if ":" in directory and directory[1] != ":":
        library_or_repo_name, relative_path = directory.split(":")
        potential_repo_path = os.path.join(
            repo.get_moban_home(), library_or_repo_name
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
