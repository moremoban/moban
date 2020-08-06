import os
import sys
import filecmp

import fs.path
from mock import patch

from moban.main import main
from .utils import Docs


class TestRegression(Docs):
    def setUp(self):
        super(TestRegression, self).setUp()
        self.base_folder = fs.path.join("tests", "regression_tests")

    def test_coping_binary_file(self):
        folder = "regr-01-copy-binary-file"
        args = ["moban"]
        self._raw_moban(
            args,
            folder,
            fs.path.join("copy-source", "image.png"),
            "regression-test.png",
        )

    def test_default_copy_as_error_handling_behavior(self):
        folder = "regr-02-templating-failure-results-in-copy-action"
        args = ["moban"]
        self._raw_moban(
            args,
            folder,
            fs.path.join("copy-source", "image.png"),
            "regression-test.png",
        )

    def test_level_7(self):
        expected = "YWJj\n"

        folder = "level-7-plugin-dir-cli"
        self.run_moban(
            [
                "moban",
                "-td",
                "my-templates/",
                "-t",
                "filter.jj2",
                "-pd",
                "custom-jj2-plugin",
                "-o",
                "moban.output",
            ],
            folder,
            [("moban.output", expected)],
        )

    def test_level_7_b(self):
        expected = "1\n2\n3\n4\n5\n6\n8\n"

        folder = "level-7-b-template-engine-plugin"
        self.run_moban(
            [
                "moban",
                "--template-type",
                "de-duplicate",
                "-pd",
                "custom-plugin",
                "-t",
                "duplicated_content.txt",
                "-o",
                "moban.output",
            ],
            folder,
            [("moban.output", expected)],
        )

    def test_level_21_copy_templates_into_tars(self):
        expected = "test file\n"

        folder = "level-21-b-copy-templates-into-a-tar"
        long_url = (
            "tar://my.tar!/test-recursive-dir/sub_directory_is_copied"
            + "/because_star_star_is_specified.txt"
        )
        criterias = [
            ["tar://my.tar!/simple.file", expected],
            [
                "tar://my.tar!/target_without_template_type",
                "file extension will trigger copy engine\n",
            ],
            [
                "tar://my.tar!/target_in_short_form",
                (
                    "it is OK to have a short form, "
                    + "but the file to be 'copied' shall have 'copy' extension, "
                    + "so as to trigger ContentForwardEngine, 'copy' engine.\n"
                ),
            ],
            ["tar://my.tar!/test-dir/afile.txt", "dir for copying\n"],
            [long_url, "dest_directory: source_directory/**\n"],
        ]
        self.run_moban_with_fs(["moban"], folder, criterias)

    def test_level_21_copy_templates_from_tars(self):
        expected = "test file\n"

        folder = "level-21-c-copy-templates-from-a-tar"
        long_url = (
            "zip://my.zip!/test-recursive-dir/sub_directory_is_copied"
            + "/because_star_star_is_specified.txt"
        )
        criterias = [
            ["zip://my.zip!/simple.file", expected],
            [
                "zip://my.zip!/target_without_template_type",
                "file extension will trigger copy engine\n",
            ],
            [
                "zip://my.zip!/target_in_short_form",
                (
                    "it is OK to have a short form, "
                    + "but the file to be 'copied' shall have 'copy' extension, "
                    + "so as to trigger ContentForwardEngine, 'copy' engine.\n"
                ),
            ],
            ["zip://my.zip!/test-dir/afile.txt", "dir for copying\n"],
            [long_url, "dest_directory: source_directory/**\n"],
        ]
        self.run_moban_with_fs(["moban"], folder, criterias)

    def _raw_moban(self, args, folder, expected, output):
        base_dir = fs.path.join("tests", "regression_tests")
        os.chdir(fs.path.join(base_dir, folder))
        with patch.object(sys, "argv", args):
            main()
        status = filecmp.cmp(output, expected)
        os.unlink(output)
        assert status
