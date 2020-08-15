import os
import logging
from collections import defaultdict

from fs.errors import ResourceNotFound
from lml.plugin import PluginManager

from moban import constants, exceptions
from moban.core import utils
from moban.externals import reporter, file_system
from moban.deprecated import deprecated_moban_path_notation
from moban.core.context import Context
from moban.core.strategy import Strategy
from moban.core.hashstore import HASH_STORE
from moban.core.definitions import TemplateTarget
from moban.externals.buffered_writer import BufferedWriter

LOG = logging.getLogger(__name__)


class MobanFactory(PluginManager):
    def __init__(self):
        super(MobanFactory, self).__init__(constants.TEMPLATE_ENGINE_EXTENSION)
        self.extensions = defaultdict(set)
        self.options_registry = {}

    def register_extensions(self, extensions):
        for user_template_type in extensions.keys():
            template_type = self.get_primary_key(user_template_type)

            LOG.debug(
                "Registering extensions: {0}={1}".format(
                    user_template_type, extensions[user_template_type]
                )
            )
            if template_type in self.extensions:
                self.extensions[template_type] = self.extensions[
                    user_template_type
                ].union(extensions[user_template_type])
            else:
                self.extensions[template_type] = extensions[user_template_type]

    def register_options(self, template_types):
        # need the value of 'template_types'
        # see test_get_user_defined_engine for help
        self.options_registry.update(template_types)

    def get_engine(self, template_type, template_dirs, context_dirs):
        template_dirs = list(expand_template_directories(template_dirs))
        template_dirs = utils.verify_the_existence_of_directories(
            template_dirs
        )
        if template_type in self.options_registry:

            custom_engine_spec = self.options_registry[template_type]
            engine_cls = self.load_me_now(
                custom_engine_spec[constants.TEMPLATE_TYPES_BASE_TYPE]
            )
            options = custom_engine_spec[constants.TEMPLATE_TYPES_OPTIONS]
        else:
            engine_cls = self.load_me_now(template_type)
            engine_extensions = self.extensions.get(template_type)
            if engine_extensions:
                options = dict(extensions=list(engine_extensions))
            else:
                options = dict()
        template_fs = file_system.get_multi_fs(template_dirs)
        engine = engine_cls(template_fs, options)
        return MobanEngine(template_fs, context_dirs, engine)

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
    def __init__(self, template_fs, context_dirs, engine):
        context_dirs = expand_template_directory(context_dirs)
        self.context = Context(context_dirs)
        self.template_fs = template_fs
        self.engine = engine
        self.templated_count = 0
        self.file_count = 0
        self.buffered_writer = BufferedWriter()
        self.engine_action = getattr(
            engine,
            "ACTION_IN_PRESENT_CONTINUOUS_TENSE",
            constants.LABEL_MOBAN_ACTION_IN_PRESENT_CONTINUOUS_TENSE,
        )
        self.engine_actioned = getattr(
            engine,
            "ACTION_IN_PAST_TENSE",
            constants.LABEL_MOBAN_ACTION_IN_PAST_TENSE,
        )
        self.fall_out_targets = []

    def report(self):
        if self.templated_count == 0:
            reporter.report_no_action()
        elif self.templated_count == self.file_count:
            reporter.report_full_run(self.engine_actioned, self.file_count)
        else:
            reporter.report_partial_run(
                self.engine_actioned, self.templated_count, self.file_count
            )

    def number_of_templated_files(self):
        return self.templated_count

    def render_to_file(self, template_file, data_file, output_file):
        data = self.context.get_data(data_file)
        template = self.engine.get_template(template_file)
        try:
            template_abs_path = self.template_fs.geturl(
                template_file, purpose="fs"
            )
        except ResourceNotFound:
            template_abs_path = template_file

        flag = self.apply_template(
            template_abs_path, template, data, output_file
        )
        if flag:
            reporter.report_templating(
                self.engine_action, template_file, output_file
            )
            self.templated_count += 1
        self.file_count += 1

        self.buffered_writer.close()

    def render_string_to_file(
        self, template_in_string, data_file, output_file
    ):
        template = self.engine.get_template_from_string(template_in_string)
        template_abs_path = f"{template_in_string[:10]}..."
        data = self.context.get_data(data_file)
        flag = self.apply_template(
            template_abs_path, template, data, output_file
        )
        if flag:
            reporter.report_templating(
                self.engine_action, template_abs_path, output_file
            )
            self.templated_count += 1
        self.file_count += 1
        self.buffered_writer.close()

    def apply_template(self, template_abs_path, template, data, output_file):

        # render the content
        rendered_content = self.engine.apply_template(
            template, data, output_file
        )

        # convert to utf8 if not already
        if not isinstance(rendered_content, bytes):
            rendered_content = rendered_content.encode("utf-8")

        # attempt to output to the file and printing to stdout instead
        # if not found
        try:

            # check if any of the files have changed
            flag = HASH_STORE.is_file_changed(
                output_file, rendered_content, template_abs_path
            )

            # if they have re-render things
            if flag:

                # write the content to the output file
                self.buffered_writer.write_file_out(
                    output_file, rendered_content
                )

                # attempt to copy the file permissions of the template
                # file to the output file

                # if it isn't an archive proceed or stdout
                if (
                    not file_system.is_zip_alike_url(output_file)
                    and output_file != "-"
                ):

                    try:
                        file_system.file_permissions_copy(
                            template_abs_path, output_file
                        )
                    except exceptions.NoPermissionsNeeded:
                        # HttpFs does not have getsyspath
                        # zip, tar have no permission
                        # win32 does not work
                        pass
            return flag
        except exceptions.FileNotFound:
            # the template is a string from command line
            LOG.info(f"{template_abs_path} is not a file")
            self.buffered_writer.write_file_out(output_file, rendered_content)
            return True

    def render_to_files(self, array_of_template_targets):
        sta = Strategy(array_of_template_targets)

        sta.process()
        choice = sta.what_to_do()
        if choice == Strategy.DATA_FIRST:
            self._render_with_finding_data_first(sta.data_file_index)
        else:
            self._render_with_finding_template_first(sta.template_file_index)
        self.buffered_writer.close()

    def _render_with_finding_template_first(self, template_file_index):
        for (template_file, data_output_pairs) in template_file_index.items():
            try:
                template = self.engine.get_template(template_file)
                template_abs_path = self.template_fs.geturl(
                    template_file, purpose="fs"
                )
                for (data_file, output) in data_output_pairs:
                    data = self.context.get_data(data_file)
                    flag = self.apply_template(
                        template_abs_path, template, data, output
                    )
                    if flag:
                        reporter.report_templating(
                            self.engine_action, template_file, output
                        )
                        self.templated_count += 1
                    self.file_count += 1
            except exceptions.PassOn:
                for (data_file, output) in data_output_pairs:
                    self.fall_out_targets.append(
                        TemplateTarget(
                            template_file,
                            data_file,
                            output,
                            template_type=constants.TEMPLATE_COPY,
                        )
                    )
                    reporter.report_info_message(
                        f"{self.engine_action} is switched to copy:"
                        + f" {template_file} to {output}"
                    )
                continue

    def _render_with_finding_data_first(self, data_file_index):
        for (data_file, template_output_pairs) in data_file_index.items():
            data = self.context.get_data(data_file)
            for (template_file, output) in template_output_pairs:
                try:
                    template = self.engine.get_template(template_file)

                    if isinstance(template, bool):
                        if template:
                            reporter.report_templating(
                                self.engine_action, template_file, None
                            )
                            self.templated_count += 1
                    else:
                        template_abs_path = self.template_fs.geturl(
                            template_file, purpose="fs"
                        )
                        flag = self.apply_template(
                            template_abs_path, template, data, output
                        )
                        if flag:
                            reporter.report_templating(
                                self.engine_action, template_file, output
                            )
                            self.templated_count += 1
                    self.file_count += 1
                except exceptions.PassOn:
                    self.fall_out_targets.append(
                        TemplateTarget(
                            template_file,
                            data_file,
                            output,
                            template_type=constants.TEMPLATE_COPY,
                        )
                    )

                    reporter.report_info_message(
                        f"{self.engine_action} is switched to copy:"
                        + f" {template_file} to {output}"
                    )
                    continue


def expand_template_directories(dirs):
    LOG.debug(f"Expanding {dirs}...")
    if not isinstance(dirs, list):
        dirs = [dirs]

    for directory in dirs:
        yield expand_template_directory(directory)


def expand_template_directory(directory):
    LOG.debug(f"Expanding {directory}...")
    translated_directory = None
    if ":" in directory and directory[1] != ":" and "://" not in directory:
        translated_directory = deprecated_moban_path_notation(directory)
    elif "://" in directory:
        translated_directory = directory
    else:
        # local template path
        translated_directory = os.path.normcase(os.path.abspath(directory))
        translated_directory = file_system.fs_url(translated_directory)
    return translated_directory
