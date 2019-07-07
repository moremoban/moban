import os

from nose.tools import eq_, raises
from moban.data_loaders.yaml import open_yaml
from moban.data_loaders.manager import load_data


def test_simple_yaml():
    test_file = os.path.join("tests", "fixtures", "simple.yaml")
    data = open_yaml(test_file)
    eq_(data, {"simple": "yaml"})


def test_inheritance_yaml():
    test_file = os.path.join("tests", "fixtures", "child.yaml")
    data = load_data(os.path.join("tests", "fixtures", "config"), test_file)
    eq_(data, {"key": "hello world", "pass": "ox"})


@raises(IOError)
def test_exception():
    test_file = os.path.join("tests", "fixtures", "orphan.yaml")
    load_data(os.path.join("tests", "fixtures", "config"), test_file)


@raises(IOError)
def test_exception_2():
    test_file = os.path.join("tests", "fixtures", "dragon.yaml")
    load_data(os.path.join("tests", "fixtures", "config"), test_file)


@raises(IOError)
def test_exception_3():
    test_file = os.path.join("tests", "fixtures", "dragon.yaml")
    load_data(None, test_file)
