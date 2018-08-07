import os
import sys

from nose.tools import eq_

from mock import patch
from moban.main import main


class TestTutorial:
    def setUp(self):
        self.current = os.getcwd()

    def test_level_1(self):
        expected = "world"
        folder = "level-1-jinja2-cli"
        self._moban(folder, expected)

    def test_level_2(self):
        expected = """========header============

world

========footer============
"""
        folder = "level-2-template-inheritance"
        self._moban(folder, expected)

    def test_level_3(self):
        expected = """========header============

world

shijie

========footer============
"""
        folder = "level-3-data-override"
        self._moban(folder, expected)

    def test_level_4(self):
        expected = """========header============

world

shijie

========footer============
"""
        folder = "level-4-single-command"
        self._raw_moban(["moban"], folder, expected, "a.output")

    def test_level_5(self):
        expected = """========header============

world

shijie

this demonstrates jinja2's include statement

========footer============
"""
        folder = "level-5-custom-configuration"
        self._raw_moban(["moban"], folder, expected, "a.output")

    def test_level_6(self):
        expected = """========header============

world2

shijie

this demonstrates jinja2's include statement

========footer============
"""
        folder = "level-6-complex-configuration"
        self._raw_moban(["moban"], folder, expected, "a.output2")

    def test_level_7(self):
        expected = """Hello, you are in level 7 example

Hello, you are not in level 7
"""
        folder = "level-7-use-custom-jinja2-filter-test-n-global"
        self._raw_moban(["moban"], folder, expected, "test.output")

    def test_level_8(self):
        expected = "it is a test\n"
        folder = "level-8-pass-a-folder-full-of-templates"
        self._raw_moban(["moban"], folder, expected, "templated-folder/my")

    def test_level_9(self):
        expected = "moban dependency as pypi package"
        folder = "level-9-moban-dependency-as-pypi-package"
        self._raw_moban(["moban"], folder, expected, "test.txt")

    def test_misc_1(self):
        expected = "test file\n"

        folder = "misc-1-copying-templates"
        self._raw_moban(["moban"], folder, expected, "simple.file.copy")

    def _moban(self, folder, expected):
        args = ["moban", "-c", "data.yml", "-t", "a.template"]
        self._raw_moban(args, folder, expected, "moban.output")

    def _raw_moban(self, args, folder, expected, output):
        os.chdir(os.path.join("docs", folder))
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
