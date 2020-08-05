import sys

from mock import patch
from nose.tools import eq_

from moban.externals import reporter

PY2 = sys.version_info[0] == 2
if PY2:
    from StringIO import StringIO
else:
    from io import StringIO


class TestReporter:
    def setUp(self):
        reporter.GLOBAL["PRINT"] = True

    def test_partial_run(self):
        patcher = patch("sys.stdout", new_callable=StringIO)
        fake_stdout = patcher.start()
        reporter.report_partial_run("Actioned", 1, 20)
        patcher.stop()
        eq_(fake_stdout.getvalue(), "Actioned 1 out of 20 files.\n")

    def test_full_run(self):
        patcher = patch("sys.stdout", new_callable=StringIO)
        fake_stdout = patcher.start()
        reporter.report_full_run("Worked on", 20)
        patcher.stop()
        eq_(fake_stdout.getvalue(), "Worked on 20 files.\n")

    def test_error_message(self):
        patcher = patch("sys.stderr", new_callable=StringIO)
        fake_stdout = patcher.start()
        reporter.report_error_message("something wrong")
        patcher.stop()
        eq_(fake_stdout.getvalue(), "Error: something wrong\n")

    def test_info_message(self):
        patcher = patch("sys.stdout", new_callable=StringIO)
        fake_stdout = patcher.start()
        reporter.report_info_message("for your information")
        patcher.stop()
        eq_(fake_stdout.getvalue(), "Info: for your information\n")

    def test_warning_message(self):
        patcher = patch("sys.stderr", new_callable=StringIO)
        fake_stdout = patcher.start()
        reporter.report_warning_message("Maybe you wanna know")
        patcher.stop()
        eq_(fake_stdout.getvalue(), "Warning: Maybe you wanna know\n")

    def test_report_templating(self):
        patcher = patch("sys.stdout", new_callable=StringIO)
        fake_stdout = patcher.start()
        reporter.report_templating("Transforming", "a", "b")
        patcher.stop()
        eq_(fake_stdout.getvalue(), "Transforming a to b\n")

    def test_no_action(self):
        patcher = patch("sys.stdout", new_callable=StringIO)
        fake_stdout = patcher.start()
        reporter.report_no_action()
        patcher.stop()
        eq_(fake_stdout.getvalue(), "No actions performed\n")

    def test_format_single(self):
        message = "1 files"
        ret = reporter._format_single(message, 1)
        eq_(ret, "1 file")

    def test_report_template_not_in_moban_file(self):
        patcher = patch("sys.stderr", new_callable=StringIO)
        fake_stdout = patcher.start()
        reporter.report_template_not_in_moban_file("test.jj2")
        patcher.stop()
        eq_(
            fake_stdout.getvalue(),
            "Warning: test.jj2 is not defined in your moban file!\n",
        )

    def test_report_file_extension_not_needed(self):
        patcher = patch("sys.stdout", new_callable=StringIO)
        fake_stdout = patcher.start()
        reporter.report_file_extension_not_needed()
        patcher.stop()
        eq_(
            fake_stdout.getvalue(),
            "Info: File extension is not required for ad-hoc type\n",
        )
