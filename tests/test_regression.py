import os
import sys
import filecmp
from textwrap import dedent

import fs.path
from mock import patch
from moban.main import main

from . import utils


def custom_dedent(long_texts):
    refined = dedent(long_texts)
    if refined.startswith("\n"):
        refined = refined[1:]
    return refined


class TestRegression(utils.Docs):
    def test_coping_binary_file(self):
        folder = "regr-01-copy-binary-file"
        args = ["moban"]
        self._raw_moban(
            args,
            folder,
            fs.path.join("copy-source", "image.png"),
            "regression-test.png",
        )

    def test_level_21_copy_templates_into_tars(self):
        expected = "test file\n"

        folder = "level-21-b-copy-templates-into-a-tar"
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
        ]
        self._raw_moban_with_fs2(["moban"], folder, criterias)

    def test_level_21_copy_templates_from_tars(self):
        expected = "test file\n"

        folder = "level-21-c-copy-templates-from-a-tar"
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
        ]
        self._raw_moban_with_fs2(["moban"], folder, criterias)

    def _raw_moban(self, args, folder, expected, output):
        base_dir = fs.path.join("tests", "regression_tests")
        os.chdir(fs.path.join(base_dir, folder))
        with patch.object(sys, "argv", args):
            main()
        status = filecmp.cmp(output, expected)
        os.unlink(output)
        assert status

    def _raw_moban_with_fs(self, args, folder, expected, output):
        base_dir = fs.path.join("tests", "regression_tests")
        os.chdir(fs.path.join(base_dir, folder))
        utils.run_moban_with_fs(args, folder, [(output, expected)])

    def _raw_moban_with_fs2(self, args, folder, criterias):
        base_dir = fs.path.join("tests", "regression_tests")
        os.chdir(fs.path.join(base_dir, folder))
        utils.run_moban_with_fs(args, folder, criterias)
