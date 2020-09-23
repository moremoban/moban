import os

import pytest

from moban.externals import file_system
from moban.plugins.jinja2.engine import Engine


def test_jinja2_template():
    path = fs.path.join("tests", "fixtures", "jinja_tests")
    fs = file_system.get_multi_fs([path])
    engine = Engine(fs)
    template = engine.get_template("file_tests.template")
    data = dict(test="here")
    result = engine.apply_template(template, data, None)
    expected = "yes\nhere"
    assert expected == result


def test_jinja2_template_string():
    path = fs.path.join("tests", "fixtures", "jinja_tests")
    fs = file_system.get_multi_fs([path])
    engine = Engine(fs)
    template = engine.get_template_from_string("{{test}}")
    data = dict(test="here")
    result = engine.apply_template(template, data, None)
    expected = "here"
    assert expected == result
