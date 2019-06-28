import os

from nose.tools import eq_
from moban.plugins.context import Context


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


def test_json_data_overrides_environ_variables():
    test_var = "TEST_ENVIRONMENT_VARIABLE"
    test_value = "am I found"
    os.environ[test_var] = test_value
    context = Context(os.path.join("tests", "fixtures"))
    data = context.get_data("simple.json")
    eq_(data[test_var], test_value)


def test_unknown_data_file():
    test_var = "TEST_ENVIRONMENT_VARIABLE"
    test_value = "am I found"
    os.environ[test_var] = test_value
    context = Context(os.path.join("tests", "fixtures"))
    data = context.get_data("unknown.data")
    eq_(data[test_var], test_value)
