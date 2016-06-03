from nose.tools import raises

from moban.engine import EngineFactory, Engine


def test_default_template_type():
    engine_class = EngineFactory.get_engine("jinja2")
    assert engine_class == Engine


def test_default_mako_type():  # fake mako
    engine_class = EngineFactory.get_engine("mako")
    assert engine_class == Engine


@raises(NotImplementedError)
def test_unknown_template_type():
    EngineFactory.get_engine("unknown_template_type")
