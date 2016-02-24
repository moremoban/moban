import os
from mock import patch
from moban.template import do_templates


@patch("moban.template.do_templates_with_more_shared_data")
def test_do_templates_1(_do_templates_with_more_shared_data):
    jobs = [
        ('data.yml', '1.template', '1.output'),
        ('data.yml', '2.template', '2.output'),
        ('data.yml', '3.template', '3.output'),
        ('data.yml', '4.template', '4.output'),
        ('data.yml', '5.template', '6.output'),
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
    options = {}
    do_templates(options, jobs)
    _do_templates_with_more_shared_data.assert_called_with(options, expected)


@patch("moban.template.do_templates_with_more_shared_templates")
def test_do_templates_2(_do_templates_with_more_shared_templates):
    jobs = [
        ('data1.yml', '1.template', '1.output'),
        ('data2.yml', '1.template', '2.output'),
        ('data3.yml', '1.template', '3.output'),
        ('data4.yml', '1.template', '4.output'),
        ('data5.yml', '1.template', '6.output'),
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
    options = {}
    do_templates(options, jobs)
    _do_templates_with_more_shared_templates.assert_called_with(options, expected)


def test_do_templates_with_more_shared_templates():
    from moban.template import do_templates_with_more_shared_templates
    base_dir = os.path.join("tests", "fixtures")
    options = {
        "configuration_dir": os.path.join(base_dir, "config"),
        "template_dir": base_dir
    }
    do_templates_with_more_shared_templates(options, {
        "a.template": [(os.path.join(base_dir, "child.yaml"),
         'test')]
    })
    with open("test", "r") as f:
        content = f.read()
        assert content == "hello world ox"
    os.unlink("test")


def test_do_templates_with_more_shared_data():
    from moban.template import do_templates_with_more_shared_data
    base_dir = os.path.join("tests", "fixtures")
    options = {
        "configuration_dir": os.path.join(base_dir, "config"),
        "template_dir": base_dir
    }
    do_templates_with_more_shared_data(options, {
        os.path.join(base_dir, "child.yaml"): [("a.template", 'test')]
    })
    with open("test", "r") as f:
        content = f.read()
        assert content == "hello world ox"
    os.unlink("test")