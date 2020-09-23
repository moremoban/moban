import pytest
import fs.path

from moban.core.data_loader import load_data
from moban.plugins.yaml_loader import open_yaml


def test_simple_yaml():
    test_file = fs.path.join("tests", "fixtures", "simple.yaml")
    data = open_yaml(test_file)
    assert data == {"simple": "yaml"}


def test_inheritance_yaml():
    test_file = fs.path.join("tests", "fixtures", "child.yaml")
    data = load_data(fs.path.join("tests", "fixtures", "config"), test_file)
    assert data == {"key": "hello world", "pass": "ox"}


def test_exception():
    test_file = fs.path.join("tests", "fixtures", "orphan.yaml")
    data = load_data(fs.path.join("tests", "fixtures", "config"), test_file)
    assert len(data) == 0


def test_exception_2():
    test_file = fs.path.join("tests", "fixtures", "dragon.yaml")
    with pytest.raises(IOError):
        load_data(fs.path.join("tests", "fixtures", "config"), test_file)


def test_exception_3():
    test_file = fs.path.join("tests", "fixtures", "dragon.yaml")
    with pytest.raises(IOError):
        load_data(None, test_file)
