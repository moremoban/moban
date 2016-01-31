import os
import sys
from moban.template import main
from mock import patch
from argparse import Namespace
from nose.tools import raises


@patch("moban.template.do_template")
def test_default_options(fake_template_doer):
    test_args = ["moban", "-c", "config.yaml",
                 "-t", "a.template"]
    with patch.object(sys, 'argv', test_args):
        main()
        fake_template_doer.assert_called_with(Namespace(
            template="a.template",
            configuration="config.yaml",
            configuration_dir=os.path.join('.', 'config'),
            output="a.output",
            template_dir=[".", os.path.join('.', 'templates')],
        ))


@patch("moban.template.do_template")
def test_custom_options(fake_template_doer):
    test_args = ["moban", "-c", "config.yaml",
                 "-cd", "/home/developer/configuration",
                 "-td", "/home/developer/templates",
                 "-t", "a.template"]
    with patch.object(sys, 'argv', test_args):
        main()
        fake_template_doer.assert_called_with(Namespace(
            template="a.template",
            configuration="config.yaml",
            configuration_dir="/home/developer/configuration",
            output="a.output",
            template_dir=['/home/developer/templates'],
        ))


@raises(SystemExit)
def test_no_argments():
    test_args = ["moban"]
    with patch.object(sys, 'argv', test_args):
        main()


@raises(SystemExit)
def test_missing_configuration():
    test_args = ["moban", '-t', "a.template"]
    with patch.object(sys, 'argv', test_args):
        main()


@raises(SystemExit)
def test_missing_template():
    test_args = ["moban", '-c', "a.config"]
    with patch.object(sys, 'argv', test_args):
        main()
