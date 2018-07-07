import os
from moban.copier import Copier
from moban.mobanfile import handle_copy
from nose.tools import eq_
from mock import patch
import shutil


class TestCopier:

    def setUp(self):
        self.patcher = patch("shutil.copy")
        self.fake_copy = self.patcher.start()

    def tearDown(self):
        self.patcher.stop()

    @patch("moban.reporter.report_copying")
    def test_copy_files(self, reporter):
        copier = Copier([os.path.join("tests", "fixtures")])
        file_list = [{"/tmp/test": "copier-test01.csv"}]
        copier.copy_files(file_list)
        self.fake_copy.assert_called()

    @patch("moban.reporter.report_error_message")
    def test_copy_files_file_not_found(self, reporter):
        copier = Copier([os.path.join("tests", "fixtures")])
        file_list = [{"/tmp/test": "copier-test-not-found.csv"}]
        copier.copy_files(file_list)
        reporter.assert_called_with(
            "copier-test-not-found.csv cannot be found"
        )

    def test_number_of_files(self):
        copier = Copier([os.path.join("tests", "fixtures")])
        file_list = [{"/tmp/test": "copier-test04.csv"}]
        copier.copy_files(file_list)
        eq_(copier.number_of_copied_files(), 1)

    def test_handle_copy(self):
        tmpl_dirs = [os.path.join("tests", "fixtures")]
        copy_config = [{"/tmp/test": "copier-test05.csv"}]
        count = handle_copy(tmpl_dirs, copy_config)
        eq_(count, 1)


@patch("moban.reporter.report_copying")
def test_lazy_copy_files(reporter):
    copier = Copier([os.path.join("tests", "fixtures")])
    file_list = [{"/tmp/test2": "copier-test02.csv"}]
    copier.copy_files(file_list)
    copier.copy_files(file_list)  # not called the second time
    eq_(reporter.call_count, 1)
    os.unlink("/tmp/test2")


@patch("moban.reporter.report_copying")
def test_copy_dir(reporter):
    test_dir = "/tmp/copy-a-directory"
    copier = Copier([os.path.join("tests", "fixtures")])
    file_list = [{test_dir: "copier-directory"}]
    copier.copy_files(file_list)
    copier.copy_files(file_list)  # not called the second time
    eq_(reporter.call_count, 2)
    shutil.rmtree(test_dir)
