import os

from nose.tools import eq_
from moban.plugins import Context


def test_context():
    context = Context(os.path.join("tests", "fixtures"))
    data = context.get_data("simple.yaml")
    eq_(data["simple"], "yaml")


def test_environ_variables():
    test_var = "TEST_ENVIRONMENT_VARIABLE"
    test_value = "am I found"
    os.environ[test_var] = test_value
    context = Context(os.path.join("tests", "fixtures"))
    data = context.get_data("simple.yaml")
    eq_(data[test_var], test_value)
