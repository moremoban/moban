import os

from nose.tools import eq_
from moban.jinja2.engine import Engine


def test_jinja2_template():
    path = os.path.join("tests", "fixtures", "jinja_tests")
    engine = Engine([path])
    template = engine.get_template("file_tests.template")
    data = dict(test="here")
    result = engine.apply_template(template, data, None)
    expected = "yes\nhere"
    eq_(expected, result)


def test_jinja2_template_string():
    path = os.path.join("tests", "fixtures", "jinja_tests")
    engine = Engine([path])
    template = engine.get_template_from_string("{{test}}")
    data = dict(test="here")
    result = engine.apply_template(template, data, None)
    expected = "here"
    eq_(expected, result)
