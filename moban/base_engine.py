import os
import moban.utils as utils
import moban.reporter as reporter
from moban.engine_factory import Strategy


class BaseEngine(object):
    def __init__(self):
        self.templated_count = 0
        self.file_count = 0

    def render_to_files(self, array_of_param_tuple):
        sta = Strategy(array_of_param_tuple)
        sta.process()
        choice = sta.what_to_do()
        if choice == Strategy.DATA_FIRST:
            self._render_with_finding_data_first(sta.data_file_index)
        else:
            self._render_with_finding_template_first(sta.template_file_index)

    def report(self):
        if self.templated_count == 0:
            reporter.report_no_action()
        elif self.templated_count == self.file_count:
            reporter.report_full_run(self.file_count)
        else:
            reporter.report_partial_run(
                self.templated_count, self.file_count
            )

    def number_of_templated_files(self):
        return self.templated_count

    def _file_permissions_copy(self, template_file, output_file):
        true_template_file = template_file
        for a_template_dir in self.template_dirs:
            true_template_file = os.path.join(a_template_dir, template_file)
            if os.path.exists(true_template_file):
                break
        utils.file_permissions_copy(true_template_file, output_file)
