import os
from nose.tools import raises
from moban.template import open_yaml


def test_simple_yaml():
    test_file = os.path.join("tests", "fixtures", "simple.yaml")
    data = open_yaml(os.path.join("tests", "fixtures"), test_file)
    assert data=={
        "simple": "yaml"
    }


def test_inheritance_yaml():
    test_file = os.path.join("tests", "fixtures", "child.yaml")
    data = open_yaml(os.path.join("tests", "fixtures", "config"), test_file)
    assert data=={
        "key": "hello world",
        "pass": "ox"
    }


@raises(IOError)
def test_exception():
    test_file = os.path.join("tests", "fixtures", "orphan.yaml")
    open_yaml(os.path.join("tests", "fixtures", "config"),test_file)

    
@raises(IOError)
def test_exception_2():
    test_file = os.path.join("tests", "fixtures", "dragon.yaml")
    open_yaml(os.path.join("tests", "fixtures", "config"),test_file)