import os

from mock import patch
from nose.tools import eq_
from moban.plugins import ENGINES
from moban.definitions import TemplateTarget
from moban.jinja2.engine import Engine
from moban.data_loaders.yaml import open_yaml

MODULE = "moban.plugins.template"


@patch(MODULE + ".MobanEngine._render_with_finding_data_first")
def test_do_templates_1(_do_templates_with_more_shared_data):
    jobs = [
        TemplateTarget("1.template", "data.yml", "1.output"),
        TemplateTarget("2.template", "data.yml", "2.output"),
        TemplateTarget("3.template", "data.yml", "3.output"),
        TemplateTarget("4.template", "data.yml", "4.output"),
        TemplateTarget("5.template", "data.yml", "6.output"),
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
    engine = ENGINES.get_engine("jinja2", ".", ".")
    engine.render_to_files(jobs)
    _do_templates_with_more_shared_data.assert_called_with(expected)


@patch(MODULE + ".MobanEngine._render_with_finding_template_first")
def test_do_templates_2(_do_templates_with_more_shared_templates):
    jobs = [
        TemplateTarget("1.template", "data1.yml", "1.output"),
        TemplateTarget("1.template", "data2.yml", "2.output"),
        TemplateTarget("1.template", "data3.yml", "3.output"),
        TemplateTarget("1.template", "data4.yml", "4.output"),
        TemplateTarget("1.template", "data5.yml", "6.output"),
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
    engine = ENGINES.get_engine("jinja2", ".", ".")
    engine.render_to_files(jobs)
    _do_templates_with_more_shared_templates.assert_called_with(expected)


def test_do_templates_with_more_shared_templates():
    base_dir = os.path.join("tests", "fixtures")
    engine = ENGINES.get_engine(
        "jinja2", base_dir, os.path.join(base_dir, "config")
    )
    engine._render_with_finding_template_first(
        {"a.jj2": [(os.path.join(base_dir, "child.yaml"), "test")]}
    )
    with open("test", "r") as f:
        content = f.read()
        assert content == "hello world ox"
    os.unlink("test")


def test_do_templates_with_more_shared_data():
    base_dir = os.path.join("tests", "fixtures")
    engine = ENGINES.get_engine(
        "jinja2", base_dir, os.path.join(base_dir, "config")
    )
    engine._render_with_finding_data_first(
        {os.path.join(base_dir, "child.yaml"): [("a.jj2", "test")]}
    )
    with open("test", "r") as f:
        content = f.read()
        assert content == "hello world ox"
    os.unlink("test")


def test_get_user_defined_engine():
    test_fixture = os.path.join(
        "tests", "fixtures", "mobanengine", "sample_template_type.yml"
    )
    template_types = open_yaml(test_fixture)
    ENGINES.register_options(template_types["template_types"])
    engine = ENGINES.get_engine("custom_jinja", ".", ".")
    eq_(engine.engine.__class__, Engine)


def test_custom_file_extension_is_assocated_with_user_defined_engine():
    test_fixture = os.path.join(
        "tests", "fixtures", "mobanengine", "sample_template_type.yml"
    )
    template_types = open_yaml(test_fixture)
    ENGINES.register_options(template_types["template_types"])
    template_type = ENGINES.get_primary_key("demo_file_suffix")
    eq_("custom_jinja", template_type)


def test_built_in_jinja2_file_extension_still_works():
    test_fixture = os.path.join(
        "tests", "fixtures", "mobanengine", "sample_template_type.yml"
    )
    template_types = open_yaml(test_fixture)
    ENGINES.register_options(template_types["template_types"])
    template_type = ENGINES.get_primary_key("jj2")
    eq_("jinja2", template_type)
