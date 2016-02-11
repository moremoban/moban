import os
import sys
from mock import patch
from moban.template import main


def test_level_1():
    output = 'a.output'
    current = os.getcwd()
    os.chdir(os.path.join("tutorial", "level-1-jinja2-cli"))
    args = ['moban', '-c', 'data.yaml', '-t', 'a.template']
    with patch.object(sys, 'argv', args):
        main()
        with open(output, 'r') as f:
            content = f.read()
            assert content == "world"
    os.unlink(output)
    os.chdir(current)


def test_level_2():
    output = 'a.output'
    expected = """========header============

world

========footer============
"""
    current = os.getcwd()
    os.chdir(os.path.join("tutorial", "level-2-template-inheritance"))
    args = ['moban', '-c', 'data.yaml', '-t', 'a.template']
    with patch.object(sys, 'argv', args):
        main()
        with open(output, 'r') as f:
            content = f.read()
            print content
            print expected
            assert content == expected
    os.unlink(output)
    os.chdir(current)