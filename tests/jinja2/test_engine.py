import fs

from moban.externals import file_system
from moban.plugins.jinja2.engine import Engine


def test_jinja2_template():
    path = fs.path.join("tests", "fixtures", "jinja_tests")
    fsys = file_system.get_multi_fs([path])
    options = {"extensions": ["test:moban.externals.file_system.exists"]}
    engine = Engine(fsys, options)
    template = engine.get_template("file_tests.template")
    data = dict(test="here")
    result = engine.apply_template(template, data, None)
    expected = "yes\nhere"
    assert expected == result


def test_jinja2_template_string():
    path = fs.path.join("tests", "fixtures", "jinja_tests")
    fsys = file_system.get_multi_fs([path])
    engine = Engine(fsys)
    template = engine.get_template_from_string("{{test}}")
    data = dict(test="here")
    result = engine.apply_template(template, data, None)
    expected = "here"
    assert expected == result
