import os
import sys

import moban.exceptions as exceptions
from mock import patch
from lml.plugin import PluginInfo
from nose.tools import eq_, raises
from moban.plugins import ENGINES
from moban.jinja2.engine import (
    Engine,
    is_extension_list_valid,
    import_module_of_extension,
)
from moban.plugins.context import Context
from moban.plugins.template import MobanEngine, expand_template_directories

USER_HOME = os.path.join("user", "home", ".moban", "repos")


@PluginInfo("library", tags=["testmobans"])
class TestPypkg:
    def __init__(self):
        __package_path__ = os.path.dirname(__file__)
        self.resources_path = os.path.join(__package_path__, "fixtures")


def test_expand_pypi_dir():
    dirs = list(expand_template_directories("testmobans:template-tests"))
    for directory in dirs:
        assert os.path.exists(directory)


@patch("moban.repo.get_moban_home", return_value=USER_HOME)
@patch("os.path.exists", return_value=True)
def test_expand_repo_dir(_, __):
    dirs = list(expand_template_directories("git_repo:template"))

    expected = [os.path.join(USER_HOME, "git_repo", "template")]
    eq_(expected, dirs)


def test_default_template_type():
    engine = ENGINES.get_engine("jj2", [], "")
    assert engine.engine.__class__ == Engine


class FakeEngine:
    def __init__(self, template_dirs, extensions=None):
        pass


@patch("lml.plugin.PluginManager.load_me_now", return_value=FakeEngine)
def test_default_mako_type(_):  # fake mako
    engine = ENGINES.get_engine("fake", [], "")
    assert engine.engine.__class__ == FakeEngine


@raises(exceptions.NoThirdPartyEngine)
def test_unknown_template_type():
    ENGINES.get_engine("unknown_template_type", [], "")


@raises(exceptions.DirectoryNotFound)
def test_non_existent_tmpl_directries():
    MobanEngine("abc", "tests", Engine)


@raises(exceptions.DirectoryNotFound)
def test_non_existent_config_directries():
    MobanEngine("tests", "abc", Engine)


@raises(exceptions.DirectoryNotFound)
def test_non_existent_ctx_directries():
    Context(["abc"])


def test_file_tests():
    output = "test.txt"
    path = os.path.join("tests", "fixtures", "jinja_tests")
    engine = ENGINES.get_engine("jinja2", [path], path)
    engine.render_to_file("file_tests.template", "file_tests.yml", output)
    with open(output, "r") as output_file:
        content = output_file.read()
        eq_(content, "yes\nhere")
    os.unlink(output)


def test_global_template_variables():
    output = "test.txt"
    path = os.path.join("tests", "fixtures", "globals")
    engine = ENGINES.get_engine("jinja2", [path], path)
    engine.render_to_file("variables.template", "variables.yml", output)
    with open(output, "r") as output_file:
        content = output_file.read()
        eq_(content, "template: variables.template\ntarget: test.txt\nhere")
    os.unlink(output)


def test_nested_global_template_variables():
    output = "test.txt"
    path = os.path.join("tests", "fixtures", "globals")
    engine = ENGINES.get_engine("jinja2", [path], path)
    engine.render_to_file("nested.template", "variables.yml", output)
    with open(output, "r") as output_file:
        content = output_file.read()
        eq_(content, "template: nested.template\ntarget: test.txt\nhere")
    os.unlink(output)


def test_environ_variables_as_data():
    test_var = "TEST_ENVIRONMENT_VARIABLE"
    test_value = "foo"
    os.environ[test_var] = test_value
    output = "test.txt"
    path = os.path.join("tests", "fixtures", "environ_vars_as_data")
    engine = ENGINES.get_engine("jinja2", [path], path)
    engine.render_to_file("test.template", "this_does_not_exist.yml", output)
    with open(output, "r") as output_file:
        content = output_file.read()
        eq_(content, "foo")
    os.unlink(output)


def test_string_template():
    output = "test.txt"
    path = os.path.join("tests", "fixtures")
    engine = ENGINES.get_engine("jinja2", [path], path)
    engine.render_string_to_file("{{simple}}", "simple.yaml", output)
    with open(output, "r") as output_file:
        content = output_file.read()
        eq_(content, "yaml")
    os.unlink(output)


def test_extensions_validator():
    test_fixtures = [None, ["module1", "module2"], []]
    expected = [False, True, False]
    actual = []
    for fixture in test_fixtures:
        actual.append(is_extension_list_valid(fixture))

    eq_(expected, actual)


def test_import():
    extensions = [
        "jinja2.ext.do",
        "jinja2_time.TimeExtension",
        "jinja2.ext.loopcontrols",
    ]
    import_module_of_extension(extensions)
    modules = ["jinja2", "jinja2_time"]
    for module in modules:
        assert module in sys.modules
