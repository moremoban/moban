import os
import sys

import moban.utils as utils
import moban.reporter as reporter
import moban.constants as constants
import moban.exceptions as exceptions
from lml.loader import scan_plugins_regex
from lml.plugin import PluginInfo
from moban.base_engine import BaseEngine
from moban.engine_factory import (
    MOBAN_ALL,
    BUILTIN_EXENSIONS,
    Context,
    expand_template_directory,
    expand_template_directories,
    verify_the_existence_of_directories
)

from pybars import Compiler


@PluginInfo(
    constants.TEMPLATE_ENGINE_EXTENSION, tags=["handlebars", "hbs"]
)
class EngineHandlebars(BaseEngine):
    def __init__(self, template_dirs, context_dirs):
        BaseEngine.__init__(self)
        scan_plugins_regex(MOBAN_ALL, "moban", None, BUILTIN_EXENSIONS)
        template_dirs = list(expand_template_directories(template_dirs))
        verify_the_existence_of_directories(template_dirs)
        context_dirs = expand_template_directory(context_dirs)
        self.context = Context(context_dirs)
        self.template_dirs = template_dirs

    def find_template_file(self, template_file):
        for directory in self.template_dirs:
            if os.path.exists(os.path.join(directory, template_file)):
                return os.path.abspath(os.path.join(directory, template_file))
        raise exceptions.FileNotFound(template_file)

    def render_to_file(self, template_file, data_file, output_file):
        template_file = self.find_template_file(template_file)
        with open(template_file, "r") as source:
            if sys.version_info[0] < 3:
                template = Compiler().compile(unicode(source.read())) # noqa
            else:
                template = Compiler().compile(source.read())
        data = self.context.get_data(data_file)
        reporter.report_templating(template_file, output_file)

        rendered_content = ''.join(template(data))
        utils.write_file_out(output_file, rendered_content)
        self._file_permissions_copy(template_file, output_file)

    def _render_with_finding_template_first(self, template_file_index):
        for (template_file, data_output_pairs) in template_file_index.items():
            template_file = self.find_template_file(template_file)
            for (data_file, output) in data_output_pairs:
                data = self.context.get_data(data_file)
                self._apply_template(template_file, data, output)
                reporter.report_templating(template_file, output)
                self.templated_count += 1
                self.file_count += 1

    def _render_with_finding_data_first(self, data_file_index):
        for (data_file, template_output_pairs) in data_file_index.items():
            data = self.context.get_data(data_file)
            for (template_file, output) in template_output_pairs:
                template_file = self.find_template_file(template_file)
                self._apply_template(template_file, data, output)
                reporter.report_templating(template_file, output)
                self.templated_count += 1
                self.file_count += 1

    def _apply_template(self, template, data, output):
        template_file = self.find_template_file(template)
        with open(template_file, "r") as source:
            if sys.version_info[0] < 3:
                template = Compiler().compile(unicode(source.read())) # noqa
            else:
                template = Compiler().compile(source.read())
        rendered_content = ''.join(template(data))
        rendered_content = utils.strip_off_trailing_new_lines(rendered_content)
        rendered_content = rendered_content.encode("utf-8")
        utils.write_file_out(
            output, rendered_content, strip=False, encode=False
        )
        utils.file_permissions_copy(template_file, output)
