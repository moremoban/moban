import os
from nose.tools import raises, eq_
from moban.engine import ENGINES, Engine, Context
from moban.engine import get_template_path
import moban.exceptions as exceptions
from moban.extensions import jinja_global
from moban.engine import expand_template_directories


from lml.plugin import PluginInfo


@PluginInfo("library", tags=["testmobans"])
class TestPypkg:
    def __init__(self):
        __package_path__ = os.path.dirname(__file__)
        self.resources_path = os.path.join(__package_path__, "fixtures")


def test_expand_dir():
    dirs = list(expand_template_directories("testmobans:template-tests"))
    for directory in dirs:
        assert os.path.exists(directory)
from unittest.mock import Mock
import unittest


def test_default_template_type():
    engine_class = ENGINES.get_engine("jj2")
    assert engine_class == Engine


def test_default_mako_type():  # fake mako
    engine_class = ENGINES.get_engine("mako")
    assert engine_class.__name__ == "MakoEngine"


def test_get_template_path():
    temp_dirs = ['globals', 'jinja_tests']
    template_file = Mock()
    template_file.filename = 'basic.template'
    template_path = get_template_path(temp_dirs, template_file)
    unittest.TestCase.assertEqual(first=template_path, second=os.path.join(os.getcwd(), 'globals/basic.template'))


@raises(exceptions.NoThirdPartyEngine)
def test_unknown_template_type():
    ENGINES.get_engine("unknown_template_type")


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
