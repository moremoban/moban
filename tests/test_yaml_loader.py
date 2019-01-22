import os

from nose.tools import eq_, raises

from moban.plugins import load_data, make_sure_all_pkg_are_loaded
from moban.data_loader.yaml import open_yaml


def test_simple_yaml():
    test_file = os.path.join("tests", "fixtures", "simple.yaml")
    data = open_yaml(test_file)
    eq_(data, {"simple": "yaml"})


def test_inheritance_yaml():
    test_file = os.path.join("tests", "fixtures", "child.yaml")
    make_sure_all_pkg_are_loaded()
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
