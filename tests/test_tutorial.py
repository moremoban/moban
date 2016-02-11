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
    _raw_moban(['moban'], folder, expected)

    

def _moban(folder, expected):
    args = ['moban', '-c', 'data.yaml', '-t', 'a.template']
    _raw_moban(args, folder, expected)


def _raw_moban(args, folder, expected):
    output = 'a.output'
    current = os.getcwd()
    os.chdir(os.path.join("tutorial", folder))
    with patch.object(sys, 'argv', args):
        main()
        with open(output, 'r') as f:
            content = f.read()
            assert content == expected
    os.unlink(output)
    os.chdir(current)