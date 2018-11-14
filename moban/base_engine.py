import moban.reporter as reporter


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
            reporter.report_partial_run(
                self.templated_count, self.file_count
            )

    def number_of_templated_files(self):
        return self.templated_count
