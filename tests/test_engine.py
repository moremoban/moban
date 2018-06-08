import os
from nose.tools import raises, eq_
from moban.engine import EngineFactory, Engine, Context
import moban.exceptions as exceptions
from moban.extensions import jinja_global


def test_default_template_type():
    engine_class = EngineFactory.get_engine("jinja2")
    assert engine_class == Engine


def test_default_mako_type():  # fake mako
    engine_class = EngineFactory.get_engine("mako")
    assert engine_class == Engine


@raises(exceptions.NoThirdPartyEngine)
def test_unknown_template_type():
    EngineFactory.get_engine("unknown_template_type")


@raises(exceptions.DirectoryNotFound)
def test_non_existent_tmpl_directries():
    Engine("abc", "tests")


@raises(exceptions.DirectoryNotFound)
def test_non_existent_config_directries():
    Engine("tests", "abc")


@raises(exceptions.DirectoryNotFound)
def test_non_existent_ctx_directries():
    Context(["abc"])


def test_file_tests():
    output = "test.txt"
    path = os.path.join("tests", "fixtures", "jinja_tests")
    engine = Engine([path], path)
    engine.render_to_file("file_tests.template", "file_tests.yml", output)
    with open(output, "r") as output_file:
        content = output_file.read()
        eq_(content, "yes\nhere")
    os.unlink(output)


def test_globals():
    output = "globals.txt"
    test_dict = dict(hello="world")
    jinja_global("test", test_dict)
    path = os.path.join("tests", "fixtures", "globals")
    engine = Engine([path], path)
    engine.render_to_file("basic.template", "basic.yml", output)
    with open(output, "r") as output_file:
        content = output_file.read()
        eq_(content, "world\n\ntest")
    os.unlink(output)
