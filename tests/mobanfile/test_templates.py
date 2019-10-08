import fs.path
from mock import patch
from nose.tools import eq_

from moban.core.mobanfile.templates import handle_template


class TestHandleTemplateFunction:
    def setUp(self):
        self.base_dir = [fs.path.join("tests", "fixtures")]

    def test_copy_files(self):
        results = list(
            handle_template("copier-test01.csv", "/tmp/test", self.base_dir)
        )
        expected = [("copier-test01.csv", "/tmp/test", "csv")]
        eq_(expected, results)

    @patch("moban.externals.reporter.report_error_message")
    def test_file_not_found(self, reporter):
        list(
            handle_template(
                "copier-test-not-found.csv", "/tmp/test", self.base_dir
            )
        )
        reporter.assert_called_with(
            "copier-test-not-found.csv cannot be found"
        )

    def test_listing_dir(self):
        test_dir = "/tmp/copy-a-directory"
        results = list(
            handle_template("copier-directory", test_dir, self.base_dir)
        )
        expected = [
            (
                "copier-directory/level1-file1",
                fs.path.join("/tmp/copy-a-directory", "level1-file1"),
                None,
            )
        ]
        eq_(expected, results)

    def test_listing_dir_recusively(self):
        test_dir = "/tmp/copy-a-directory"
        results = list(
            handle_template("copier-directory/**", test_dir, self.base_dir)
        )
        expected = [
            (
                fs.path.join("copier-directory", "copier-sample-dir", "file1"),
                fs.path.join(
                    "/tmp/copy-a-directory", "copier-sample-dir", "file1"
                ),
                None,
            ),
            (
                fs.path.join("copier-directory", "level1-file1"),
                fs.path.join("/tmp/copy-a-directory", "level1-file1"),
                None,
            ),
        ]
        eq_(
            sorted(results, key=lambda x: x[0]),
            sorted(expected, key=lambda x: x[0]),
        )

    @patch("moban.externals.reporter.report_error_message")
    def test_listing_dir_recusively_with_error(self, reporter):
        test_dir = "/tmp/copy-a-directory"
        list(
            handle_template(
                "copier-directory-does-not-exist/**", test_dir, self.base_dir
            )
        )
        eq_(reporter.call_count, 1)
