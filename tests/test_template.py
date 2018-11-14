import os

from mock import patch
from moban.jinja2.engine import Engine
from moban.engine_handlebars import EngineHandlebars


@patch("moban.jinja2.engine.Engine._render_with_finding_data_first")
def test_do_templates_1(_do_templates_with_more_shared_data):
    jobs = [
        ("1.template", "data.yml", "1.output"),
        ("2.template", "data.yml", "2.output"),
        ("3.template", "data.yml", "3.output"),
        ("4.template", "data.yml", "4.output"),
        ("5.template", "data.yml", "6.output"),
    ]
    expected = {
        "data.yml": [
            ("1.template", "1.output"),
            ("2.template", "2.output"),
            ("3.template", "3.output"),
            ("4.template", "4.output"),
            ("5.template", "6.output"),
        ]
    }
    engine = Engine(".", ".")
    engine.render_to_files(jobs)
    _do_templates_with_more_shared_data.assert_called_with(expected)
    if os.path.exists(".moban.hashes"):
        os.unlink(".moban.hashes")


@patch("moban.jinja2.engine.Engine._render_with_finding_template_first")
def test_do_templates_2(_do_templates_with_more_shared_templates):
    jobs = [
        ("1.template", "data1.yml", "1.output"),
        ("1.template", "data2.yml", "2.output"),
        ("1.template", "data3.yml", "3.output"),
        ("1.template", "data4.yml", "4.output"),
        ("1.template", "data5.yml", "6.output"),
    ]
    expected = {
        "1.template": [
            ("data1.yml", "1.output"),
            ("data2.yml", "2.output"),
            ("data3.yml", "3.output"),
            ("data4.yml", "4.output"),
            ("data5.yml", "6.output"),
        ]
    }
    engine = Engine(".", ".")
    engine.render_to_files(jobs)
    _do_templates_with_more_shared_templates.assert_called_with(expected)
    if os.path.exists(".moban.hashes"):
        os.unlink(".moban.hashes")


def test_do_templates_with_more_shared_templates():
    base_dir = os.path.join("tests", "fixtures")
    engine = Engine(base_dir, os.path.join(base_dir, "config"))
    engine._render_with_finding_template_first(
        {"a.jj2": [(os.path.join(base_dir, "child.yaml"), "test")]}
    )
    with open("test", "r") as f:
        content = f.read()
        assert content == "hello world ox"
    os.unlink("test")
    if os.path.exists(".moban.hashes"):
        os.unlink(".moban.hashes")


def test_do_templates_with_more_shared_data():
    base_dir = os.path.join("tests", "fixtures")
    engine = Engine(base_dir, os.path.join(base_dir, "config"))
    engine._render_with_finding_data_first(
        {os.path.join(base_dir, "child.yaml"): [("a.jj2", "test")]}
    )
    with open("test", "r") as f:
        content = f.read()
        assert content == "hello world ox"
    os.unlink("test")
    if os.path.exists(".moban.hashes"):
        os.unlink(".moban.hashes")


@patch(
    "moban.engine_handlebars.EngineHandlebars."
    "_render_with_finding_data_first"
)
def test_do_templates_1_handlebars(_do_templates_with_more_shared_data):
    jobs = [
        ("1.template", "data.yml", "1.output"),
        ("2.template", "data.yml", "2.output"),
        ("3.template", "data.yml", "3.output"),
        ("4.template", "data.yml", "4.output"),
        ("5.template", "data.yml", "6.output"),
    ]
    expected = {
        "data.yml": [
            ("1.template", "1.output"),
            ("2.template", "2.output"),
            ("3.template", "3.output"),
            ("4.template", "4.output"),
            ("5.template", "6.output"),
        ]
    }
    engine = EngineHandlebars(".", ".")
    engine.render_to_files(jobs)
    _do_templates_with_more_shared_data.assert_called_with(expected)
    if os.path.exists(".moban.hashes"):
        os.unlink(".moban.hashes")


@patch(
    "moban.engine_handlebars.EngineHandlebars."
    "_render_with_finding_template_first"
)
def test_do_templates_2_handlebars(_do_templates_with_more_shared_templates):
    jobs = [
        ("1.template", "data1.yml", "1.output"),
        ("1.template", "data2.yml", "2.output"),
        ("1.template", "data3.yml", "3.output"),
        ("1.template", "data4.yml", "4.output"),
        ("1.template", "data5.yml", "6.output"),
    ]
    expected = {
        "1.template": [
            ("data1.yml", "1.output"),
            ("data2.yml", "2.output"),
            ("data3.yml", "3.output"),
            ("data4.yml", "4.output"),
            ("data5.yml", "6.output"),
        ]
    }
    engine = EngineHandlebars(".", ".")
    engine.render_to_files(jobs)
    _do_templates_with_more_shared_templates.assert_called_with(expected)
    if os.path.exists(".moban.hashes"):
        os.unlink(".moban.hashes")


def test_do_templates_with_more_shared_templates_handlebars():
    base_dir = os.path.join("tests", "fixtures")
    engine = EngineHandlebars(base_dir, os.path.join(base_dir, "config"))
    engine._render_with_finding_template_first(
        {"a.handlebars": [(os.path.join(base_dir, "child.json"), "test")]}
    )
    with open("test", "r") as f:
        content = f.read()
        assert content == "hello world ox"
    os.unlink("test")
    if os.path.exists(".moban.hashes"):
        os.unlink(".moban.hashes")


def test_do_templates_with_more_shared_data_handlebars():
    base_dir = os.path.join("tests", "fixtures")
    engine = EngineHandlebars(base_dir, os.path.join(base_dir, "config"))
    engine._render_with_finding_data_first(
        {os.path.join(base_dir, "child.json"): [("a.handlebars", "test")]}
    )
    with open("test", "r") as f:
        content = f.read()
        assert content == "hello world ox"
    os.unlink("test")
    if os.path.exists(".moban.hashes"):
        os.unlink(".moban.hashes")
