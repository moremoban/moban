from nose.tools import raises
from moban.utils import load_external_engine
from moban.engine import Engine


@raises(ImportError)
def test_load_external_engine():
    load_external_engine("unknown_template_type")


def test_load_mako_engine(): # fake mako
    module = load_external_engine("mako")
    engine_class = module.get_engine("mako")
    assert engine_class == Engine