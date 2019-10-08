import os

from nose.tools import eq_

from moban import file_system
from moban.jinja2.engine import Engine
from moban.jinja2.extensions import jinja_global
from moban.core.moban_factory import MobanEngine


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
        eq_(content, "world\n\ntest")
    os.unlink(output)
