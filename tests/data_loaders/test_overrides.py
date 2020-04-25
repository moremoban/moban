import os

from nose.tools import eq_

from moban.main import load_engine_factory_and_engines
from moban.core.data_loader import load_data


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

    eq_(len(actual), len(expected))


def test_overrides_a_list_of_config_files_but_cannot_find_them():
    base_dir = os.path.join("tests", "fixtures", "issue_126")
    actual = load_data(None, os.path.join(base_dir, "the_config.yaml"))

    expected = [("key", "value")]
    for item, expected_item in zip(actual.items(), expected):
        eq_(item, expected_item)

    eq_(len(actual), len(expected))


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


def test_overrides_select_keys_from_parent_files():
    base_dir = os.path.join("tests", "fixtures", "issue_126")
    config_dir = os.path.join(base_dir, "config")
    actual = load_data(
        config_dir, os.path.join(base_dir, "multi-key-config.yaml")
    )
    expected = [
        ("cat", "from config"),
        ("alpha", "from a"),
        ("beta", "from b"),
    ]
    for item, expected_item in zip(actual.items(), expected):
        eq_(item, expected_item)


def test_overrides_select_keys():
    base_dir = os.path.join("tests", "fixtures", "issue_126")
    config_dir = os.path.join(base_dir, "config")
    actual = load_data(
        config_dir, os.path.join(base_dir, "multi-key-config-override.yaml")
    )
    expected = [
        ("alpha", "from config"),
        ("cat", "from config"),
        ("beta", "from b"),
    ]
    for item, expected_item in zip(actual.items(), expected):
        eq_(item, expected_item)


def test_overrides_nested_keys():
    base_dir = os.path.join("tests", "fixtures", "issue_126")
    config_dir = os.path.join(base_dir, "config")
    actual = load_data(config_dir, os.path.join(base_dir, "raspberry.yaml"))
    expected = {
        "raspberry": {
            "other": "OpenGL 3.0",
            "version": 4,
            "memory": "4GB",
            "core": "quad",
            "wifi": "2.5 & 5.0 GHz",
            "USB": 3.0,
            "Bluetooth": 5.0,
        },
        "tessel": {"version": 2, "USB": "micro", "wifi": "802.11gn"},
    }

    eq_(dict(actual), expected)


def test_overrides_fs_url():
    load_engine_factory_and_engines()
    base_dir = os.path.join("tests", "fixtures")
    actual = load_data(None, os.path.join(base_dir, "override_fs_url.yaml"))
    assert "requires" in actual
