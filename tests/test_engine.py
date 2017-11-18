from nose.tools import raises
from moban.engine import EngineFactory, Engine, Context
import moban.exceptions as exceptions


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
    Engine('abc', 'tests')


@raises(exceptions.DirectoryNotFound)
def test_non_existent_config_directries():
    Engine('tests', 'abc')


@raises(exceptions.DirectoryNotFound)
def test_non_existent_ctx_directries():
    Context(['abc'])
