import fs.path
import pytest

from moban.plugins.json_loader import open_json


def test_open_json():
    content = open_json(fs.path.join("tests", "fixtures", "child.json"))
    expected = {"key": "hello world", "pass": "ox"}
    assert expected == content
