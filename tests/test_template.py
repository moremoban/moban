import os
from mock import patch
from moban.engine import Engine


@patch("moban.engine.Engine._render_with_finding_data_first")
def test_do_templates_1(_do_templates_with_more_shared_data):
    jobs = [
        ('1.template', 'data.yml', '1.output'),
        ('2.template', 'data.yml', '2.output'),
        ('3.template', 'data.yml', '3.output'),
        ('4.template', 'data.yml', '4.output'),
        ('5.template', 'data.yml', '6.output'),
    ]
    expected = {
        'data.yml': [
            ('1.template', '1.output'),
            ('2.template', '2.output'),
            ('3.template', '3.output'),
            ('4.template', '4.output'),
            ('5.template', '6.output'),
        ]
    }
    engine = Engine('.', '.')
    engine.render_to_files(jobs)
    _do_templates_with_more_shared_data.assert_called_with(expected)


@patch("moban.engine.Engine._render_with_finding_template_first")
def test_do_templates_2(_do_templates_with_more_shared_templates):
    jobs = [
        ('1.template', 'data1.yml', '1.output'),
        ('1.template', 'data2.yml', '2.output'),
        ('1.template', 'data3.yml', '3.output'),
        ('1.template', 'data4.yml', '4.output'),
        ('1.template', 'data5.yml', '6.output'),
    ]
    expected = {
        '1.template': [
            ('data1.yml', '1.output'),
            ('data2.yml', '2.output'),
            ('data3.yml', '3.output'),
            ('data4.yml', '4.output'),
            ('data5.yml', '6.output'),
        ]
    }
    engine = Engine('.', '.')
    engine.render_to_files(jobs)
    _do_templates_with_more_shared_templates.assert_called_with(expected)


def test_do_templates_with_more_shared_templates():
    base_dir = os.path.join("tests", "fixtures")
    engine = Engine(base_dir, os.path.join(base_dir, "config"))
    engine._render_with_finding_template_first({
        "a.template": [(os.path.join(base_dir, "child.yaml"),
                        'test')]
    })
    with open("test", "r") as f:
        content = f.read()
        assert content == "hello world ox"
    os.unlink("test")


def test_do_templates_with_more_shared_data():
    base_dir = os.path.join("tests", "fixtures")
    engine = Engine(base_dir, os.path.join(base_dir, "config"))
    engine._render_with_finding_data_first({
        os.path.join(base_dir, "child.yaml"): [("a.template", 'test')]
    })
    with open("test", "r") as f:
        content = f.read()
        assert content == "hello world ox"
    os.unlink("test")
