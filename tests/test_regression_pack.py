import os
import sys
from textwrap import dedent

from mock import patch
from nose.tools import eq_
from nose import SkipTest

from moban.main import main


def custom_dedent(long_texts):
    refined = dedent(long_texts)
    if refined.startswith("\n"):
        refined = refined[1:]
    return refined


class TestTutorial:
    def setUp(self):
        self.current = os.getcwd()

    def test_symbolic_link_on_windows(self):
        if sys.platform != 'win32':
            raise SkipTest("No need to test on linux nor macos")

        expected = "test file\n"

        folder = "symbolic-link-gets-junk"
        self._raw_moban(["moban"], folder, expected, "simple.file")

    def _moban(self, folder, expected):
        args = ["moban", "-c", "data.yml", "-t", "a.template"]
        self._raw_moban(args, folder, expected, "moban.output")

    def _raw_moban(self, args, folder, expected, output):
        os.chdir(os.path.join("tests", "regression-pack", folder))
        with patch.object(sys, "argv", args):
            main()
            _verify_content(output, expected)
        os.unlink(output)

    def tearDown(self):
        if os.path.exists(".moban.hashes"):
            os.unlink(".moban.hashes")
        os.chdir(self.current)


def _verify_content(file_name, expected):
    with open(file_name, "r") as f:
        content = f.read()
        eq_(content, expected)
