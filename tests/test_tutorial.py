import os
import sys
from mock import patch
from moban.template import main


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
        self._raw_moban(['moban'], folder, expected, 'a.output')


    def test_level_5(self):
        expected = """========header============

world

shijie

this demonstrations jinja2's include statement

========footer============
"""
        folder = "level-5-custom-configuration"
        self._raw_moban(['moban'], folder, expected, 'a.output')

    def test_level_6(self):
        expected = """========header============

world2

shijie

this demonstrations jinja2's include statement

========footer============
"""
        folder = "level-6-complex-configuration"
        self._raw_moban(['moban'], folder, expected, 'a.output2')


    def _moban(self, folder, expected):
        args = ['moban', '-c', 'data.yml', '-t', 'a.template']
        self._raw_moban(args, folder, expected, 'moban.output')

    def _raw_moban(self, args, folder, expected, output):
        os.chdir(os.path.join("tutorial", folder))
        with patch.object(sys, 'argv', args):
            main()
            _verify_content(output, expected)
        os.unlink(output)

    def tearDown(self):
        os.chdir(self.current)


def _verify_content(file_name, expected):
    with open(file_name, 'r') as f:
        content = f.read()
        assert content == expected

