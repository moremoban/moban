import os
import sys
import filecmp
from textwrap import dedent

from mock import patch
from moban.main import main
from nose.tools import eq_


def custom_dedent(long_texts):
    refined = dedent(long_texts)
    if refined.startswith("\n"):
        refined = refined[1:]
    return refined


class TestRegression:
    def setUp(self):
        self.current = os.getcwd()

    def test_coping_binary_file(self):
        folder = "regr-01-copy-binary-file"
        args = ["moban"]
        self._raw_moban(
            args,
            folder,
            os.path.join("copy-source", "image.png"),
            "regression-test.png",
        )

    def _raw_moban(self, args, folder, expected, output):
        base_dir = os.path.join("tests", "regression_tests")
        os.chdir(os.path.join(base_dir, folder))
        with patch.object(sys, "argv", args):
            main()
        status = filecmp.cmp(output, expected)
        os.unlink(output)
        assert status

    def tearDown(self):
        if os.path.exists(".moban.hashes"):
            os.unlink(".moban.hashes")
        os.chdir(self.current)


def _verify_content(file_name, expected):
    with open(file_name, "r") as f:
        content = f.read()
        eq_(content, expected)
