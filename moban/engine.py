from jinja2 import Environment, FileSystemLoader
from lml.loader import scan_plugins_regex
from lml.plugin import PluginInfo

import moban.utils as utils
import moban.reporter as reporter
import moban.constants as constants
from moban.utils import get_template_path
from moban.hashstore import HASH_STORE
from moban.base_engine import BaseEngine
from moban.extensions import (
    JinjaTestManager,
    JinjaFilterManager,
    JinjaGlobalsManager
)
from moban.engine_factory import (
    MOBAN_ALL,
    BUILTIN_EXENSIONS,
    Context,
    expand_template_directory,
    expand_template_directories,
    verify_the_existence_of_directories
)

FILTERS = JinjaFilterManager()
TESTS = JinjaTestManager()
GLOBALS = JinjaGlobalsManager()


@PluginInfo(
    constants.TEMPLATE_ENGINE_EXTENSION, tags=["jinja2", "jinja", "jj2", "j2"]
)
class Engine(BaseEngine):
    def __init__(self, template_dirs, context_dirs):
        BaseEngine.__init__(self)
        scan_plugins_regex(MOBAN_ALL, "moban", None, BUILTIN_EXENSIONS)
        template_dirs = list(expand_template_directories(template_dirs))
        verify_the_existence_of_directories(template_dirs)
        context_dirs = expand_template_directory(context_dirs)
        template_loader = FileSystemLoader(template_dirs)
        self.jj2_environment = Environment(
            loader=template_loader,
            keep_trailing_newline=True,
            trim_blocks=True,
            lstrip_blocks=True,
        )
        for filter_name, filter_function in FILTERS.get_all():
            self.jj2_environment.filters[filter_name] = filter_function

        for test_name, test_function in TESTS.get_all():
            self.jj2_environment.tests[test_name] = test_function

        for global_name, dict_obj in GLOBALS.get_all():
            self.jj2_environment.globals[global_name] = dict_obj

        self.context = Context(context_dirs)
        self.template_dirs = template_dirs

    def render_to_file(self, template_file, data_file, output_file):
        template = self.jj2_environment.get_template(template_file)
        data = self.context.get_data(data_file)
        reporter.report_templating(template_file, output_file)

        rendered_content = template.render(**data)
        utils.write_file_out(output_file, rendered_content)
        self._file_permissions_copy(template_file, output_file)

    def _render_with_finding_template_first(self, template_file_index):
        for (template_file, data_output_pairs) in template_file_index.items():
            template = self.jj2_environment.get_template(template_file)
            for (data_file, output) in data_output_pairs:
                data = self.context.get_data(data_file)
                flag = self._apply_template(template, data, output)
                if flag:
                    reporter.report_templating(template_file, output)
                    self.templated_count += 1
                self.file_count += 1

    def _render_with_finding_data_first(self, data_file_index):
        for (data_file, template_output_pairs) in data_file_index.items():
            data = self.context.get_data(data_file)
            for (template_file, output) in template_output_pairs:
                template = self.jj2_environment.get_template(template_file)
                flag = self._apply_template(template, data, output)
                if flag:
                    reporter.report_templating(template_file, output)
                    self.templated_count += 1
                self.file_count += 1

    def _apply_template(self, template, data, output):
        temp_file_path = get_template_path(self.template_dirs, template)
        rendered_content = template.render(**data)
        rendered_content = utils.strip_off_trailing_new_lines(rendered_content)
        rendered_content = rendered_content.encode("utf-8")
        flag = HASH_STORE.is_file_changed(
            output, rendered_content, temp_file_path
        )
        if flag:
            utils.write_file_out(
                output, rendered_content, strip=False, encode=False
            )
            utils.file_permissions_copy(temp_file_path, output)
        return flag
