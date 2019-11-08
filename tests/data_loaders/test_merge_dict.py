from nose.tools import eq_
from ruamel.yaml import YAML

from moban.core.data_loader import merge


def test_simple_union():
    user = {"hi": "world"}
    default = {"world": "hi"}
    merged = merge(user, default)
    assert merged == {"hi": "world", "world": "hi"}


def test_simple_overlapping():
    user = {"hi": "world", "world": "hei"}
    default = {"world": "hi"}
    merged = merge(user, default)
    assert merged == {"hi": "world", "world": "hei"}


def test_two_level_merge():
    user = {"L1": {"L2": "World"}}
    default = {"L1": {"L2.1": "Hi"}}
    merged = merge(user, default)
    assert merged == {"L1": {"L2": "World", "L2.1": "Hi"}}


def test_two_level_conflict():
    user = {"L1": {"L2": "World"}}
    default = {"L1": {"L2": "Hi"}}
    merged = merge(user, default)
    assert merged == {"L1": {"L2": "World"}}


def test_three_level_conflict():
    user = {"L1": {"L2": {"L3": "World"}}}
    default = {"L1": {"L2": {"L3": "Hi"}}}
    merged = merge(user, default)
    assert merged == {"L1": {"L2": {"L3": "World"}}}


def test_merge_value_as_list():
    user = {"L1": ["a", "b"]}
    default = {"L1": ["c", "d"]}
    merged = merge(user, default)
    assert merged == {"L1": ["a", "b", "c", "d"]}


def test_merge_value_as_list_in_yaml():
    yaml = YAML(typ="rt")
    user = yaml.load(
        """
L1:
  - a
  - b
"""
    )
    default = yaml.load(
        """
L1:
  - c
  - d
"""
    )
    merged = merge(user, default)
    eq_(merged, {"L1": ["a", "b", "c", "d"]})
