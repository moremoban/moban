import os

from nose.tools import eq_
from moban.engine_handlebars import EngineHandlebars


def test_handlebars_template_not_found():
    path = os.path.join("tests", "fixtures", "handlebars_tests")
    engine = EngineHandlebars([path])
    template = engine.get_template("file_tests.template")
    data = dict(test="here")
    result = engine.apply_template(template, data, None)
    expected = "here".encode("utf-8")
    eq_(expected, result)
