import os

from nose.tools import eq_
from moban.data_loaders.manager import load_data


def test_overrides_a_list_of_config_files():
    base_dir = os.path.join("tests", "fixtures", "issue_126")
    config_dir = os.path.join(base_dir, "config")
    actual = load_data(config_dir, os.path.join(base_dir, "the_config.yaml"))
    expected = [
        ("key", "value"),
        ("key_from_a", "apple"),
        ("key_from_b", "bee"),
    ]
    for item, expected_item in zip(actual.items(), expected):
        eq_(item, expected_item)


def test_overrides_ignores_override_sequence():
    base_dir = os.path.join("tests", "fixtures", "issue_126")
    config_dir = os.path.join(base_dir, "config")
    actual = load_data(config_dir, os.path.join(base_dir, "the_config.yaml"))
    expected = [
        ("key", "value"),
        ("key_from_a", "apple"),
        ("key_from_b", "bee"),
    ]
    for item, expected_item in zip(actual.items(), expected):
        eq_(item, expected_item)
