import moban.reporter as reporter
from moban.engine_factory import Strategy


class BaseEngine(object):
    def __init__(self):
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

    def render_to_files(self, array_of_param_tuple):
        sta = Strategy(array_of_param_tuple)
        sta.process()
        choice = sta.what_to_do()
        if choice == Strategy.DATA_FIRST:
            self._render_with_finding_data_first(sta.data_file_index)
        else:
            self._render_with_finding_template_first(sta.template_file_index)
