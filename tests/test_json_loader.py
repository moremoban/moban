import os

from nose.tools import eq_

from moban.data_loader.json import open_json


def test_open_json():
    content = open_json(os.path.join("tests", "fixtures", "child.json"))
    expected = {"key": "hello world", "pass": "ox"}
    eq_(expected, content)
