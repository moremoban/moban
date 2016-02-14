import os
import sys
from mock import patch
from moban.template import main


def test_level_1():
    expected = "world"
    folder = "level-1-jinja2-cli"
    _moban(folder, expected)


def test_level_2():
    expected = """========header============

world

========footer============
"""
    folder = "level-2-template-inheritance"
    _moban(folder, expected)
    

def test_level_3():
    expected = """========header============

world

shijie

========footer============
"""
    folder = "level-3-data-override"
    _moban(folder, expected)


def test_level_4():
    expected = """========header============

world

shijie

========footer============
"""
    folder = "level-4-single-command"
    _raw_moban(['moban'], folder, expected, 'a.output')


def test_level_5():
    expected = """========header============

world

shijie

this demonstrations jinja2's include statement

========footer============
"""
    folder = "level-5-custom-configuration"
    _raw_moban(['moban'], folder, expected, 'a.output')


def _moban(folder, expected):
    args = ['moban', '-c', 'data.yml', '-t', 'a.template']
    _raw_moban(args, folder, expected, 'moban.output')


def _raw_moban(args, folder, expected, output):
    current = os.getcwd()
    os.chdir(os.path.join("tutorial", folder))
    with patch.object(sys, 'argv', args):
        main()
        with open(output, 'r') as f:
            content = f.read()
            assert content == expected
    os.unlink(output)
    os.chdir(current)
