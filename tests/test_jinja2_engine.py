import os

from nose.tools import eq_
from moban.jinja2.engine import Engine


def test_handlebars_template_not_found():
    path = os.path.join("tests", "fixtures", "jinja_tests")
    engine = Engine([path])
    template = engine.get_template("file_tests.template")
    data = dict(test="here")
    result = engine.apply_template(template, data, None)
    expected = "yes\nhere"
    eq_(expected, result)
