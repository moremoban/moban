import os
import sys
from mock import patch
from moban.template import main


def test_level_1():
    output = 'a.output'
    current = os.getcwd()
    os.chdir(os.path.join("tutorial", "level-1"))
    args = ['moban', '-c', 'data.yaml', '-t', 'a.template']
    with patch.object(sys, 'argv', args):
        main()
        with open(output, 'r') as f:
            content = f.read()
            assert content == "world"
    os.unlink(output)
    os.chdir(current)