import sys

from lml.plugin import PluginInfo

import moban.utils as utils
import moban.reporter as reporter
import moban.constants as constants
from moban import plugins
from pybars import Compiler


@PluginInfo(constants.TEMPLATE_ENGINE_EXTENSION, tags=["handlebars", "hbs"])
class EngineHandlebars(plugins.BaseEngine):

    def render_to_file(self, template_file, data_file, output_file):
        data = self.context.get_data(data_file)
        template_file, template = self._get_hbr_template(template_file)
        self._apply_template(template_file, template, data, output_file)
        reporter.report_templating(template_file, output_file)

    def _render_with_finding_template_first(self, template_file_index):
        for (template_file, data_output_pairs) in template_file_index.items():
            template_file, template = self._get_hbr_template(template_file)
            for (data_file, output) in data_output_pairs:
                data = self.context.get_data(data_file)
                self._apply_template(template_file, template, data, output)
                reporter.report_templating(template_file, output)
                self.templated_count += 1
                self.file_count += 1

    def _render_with_finding_data_first(self, data_file_index):
        for (data_file, template_output_pairs) in data_file_index.items():
            data = self.context.get_data(data_file)
            for (template_file, output) in template_output_pairs:
                template_file, template = self._get_hbr_template(template_file)
                self._apply_template(template_file, template, data, output)
                reporter.report_templating(template_file, output)
                self.templated_count += 1
                self.file_count += 1

    def _apply_template(self, template_file, template, data, output):
        rendered_content = "".join(template(data))
        rendered_content = utils.strip_off_trailing_new_lines(rendered_content)
        rendered_content = rendered_content.encode("utf-8")
        utils.write_file_out(
            output, rendered_content, strip=False, encode=False
        )
        utils.file_permissions_copy(template_file, output)

    def _get_hbr_template(self, template_file):
        actual_template_file = self.find_template_file(template_file)
        with open(actual_template_file, "r") as source:
            if sys.version_info[0] < 3:
                hbr_template = Compiler().compile(
                    unicode(source.read())  # noqa: F821
                )
            else:
                hbr_template = Compiler().compile(source.read())
        return actual_template_file, hbr_template

    def find_template_file(self, template_file):
        return utils.get_template_path(self.template_dirs, template_file)
