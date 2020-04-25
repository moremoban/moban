import fs.path
from nose.tools import eq_, raises

from moban.core.data_loader import load_data
from moban.plugins.yaml_loader import open_yaml


def test_simple_yaml():
    test_file = fs.path.join("tests", "fixtures", "simple.yaml")
    data = open_yaml(test_file)
    eq_(data, {"simple": "yaml"})


def test_inheritance_yaml():
    test_file = fs.path.join("tests", "fixtures", "child.yaml")
    data = load_data(fs.path.join("tests", "fixtures", "config"), test_file)
    eq_(data, {"key": "hello world", "pass": "ox"})


def test_exception():
    test_file = fs.path.join("tests", "fixtures", "orphan.yaml")
    data = load_data(fs.path.join("tests", "fixtures", "config"), test_file)
    eq_(len(data), 0)


@raises(IOError)
def test_exception_2():
    test_file = fs.path.join("tests", "fixtures", "dragon.yaml")
    load_data(fs.path.join("tests", "fixtures", "config"), test_file)


@raises(IOError)
def test_exception_3():
    test_file = fs.path.join("tests", "fixtures", "dragon.yaml")
    load_data(None, test_file)
