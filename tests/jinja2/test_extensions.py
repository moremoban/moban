import os

import pytest

from moban.externals import file_system
from moban.core.moban_factory import MobanEngine
from moban.plugins.jinja2.engine import Engine
from moban.plugins.jinja2.extensions import jinja_global


def test_globals():
    output = "globals.txt"
    test_dict = dict(hello="world")
    jinja_global("test", test_dict)
    path = os.path.join("tests", "fixtures", "globals")
    template_fs = file_system.get_multi_fs([path])
    engine = MobanEngine(template_fs, path, Engine(template_fs))
    engine.render_to_file("basic.template", "basic.yml", output)
    with open(output, "r") as output_file:
        content = output_file.read()
        assert content == "world\n\ntest"
    os.unlink(output)
