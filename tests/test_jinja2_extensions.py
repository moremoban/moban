import os

from nose.tools import eq_
from moban.jinja2.engine import Engine
from moban.plugins.template import MobanEngine
from moban.jinja2.extensions import jinja_global


def test_globals():
    output = "globals.txt"
    test_dict = dict(hello="world")
    jinja_global("test", test_dict)
    path = os.path.join("tests", "fixtures", "globals")
    engine = MobanEngine([path], path, Engine([path]))
    engine.render_to_file("basic.template", "basic.yml", output)
    with open(output, "r") as output_file:
        content = output_file.read()
        eq_(content, "world\n\ntest")
    os.unlink(output)
