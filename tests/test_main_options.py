import os
import sys
from shutil import copyfile
from moban.template import main
from mock import patch
from nose.tools import raises


class TestCustomOptions:
    def setUp(self):
        self.config_file = 'config.yaml'
        with open(self.config_file,'w')as f:
            f.write("hello: world")
    
    @patch("moban.template.do_template")
    def test_custom_options(self, fake_template_doer):
        test_args = ["moban", "-c", self.config_file,
                     "-cd", "/home/developer/configuration",
                     "-td", "/home/developer/templates",
                     "-t", "a.template"]
        with patch.object(sys, 'argv', test_args):
            main()
            fake_template_doer.assert_called_with(
                ['/home/developer/templates'],
                dict(hello="world"),
                [('a.template', 'a.output')]
            )
    
    @patch("moban.template.do_template")
    def test_minimal_options(self, fake_template_doer):
        test_args = ["moban", "-c", self.config_file,
                     "-t", "a.template"]
        with patch.object(sys, 'argv', test_args):
            main()
            fake_template_doer.assert_called_with(
                [".", os.path.join('.', 'templates')],
                dict(hello="world"),
                [('a.template', 'a.output')]
            )

    @raises(SystemExit)
    def test_missing_template(self):
        test_args = ["moban", '-c', self.config_file]
        with patch.object(sys, 'argv', test_args):
            main()

    def tearDown(self):
        os.unlink(self.config_file)

class TestOptions:
    def setUp(self):
        self.config_file = 'data.yaml'
        with open(self.config_file,'w')as f:
            f.write("hello: world")
    
    @patch("moban.template.do_template")
    def test_default_options(self, fake_template_doer):
        test_args = ["moban", "-t", "a.template"]
        with patch.object(sys, 'argv', test_args):
            main()
            fake_template_doer.assert_called_with(
                [".", os.path.join('.', 'templates')],
                dict(hello="world"),
                [('a.template', 'a.output')]
            )

    @raises(SystemExit)
    def test_no_argments(self):
        test_args = ["moban"]
        with patch.object(sys, 'argv', test_args):
            main()

    def tearDown(self):
        os.unlink(self.config_file)


@raises(IOError)
def test_missing_configuration():
    test_args = ["moban", '-t', "a.template"]
    with patch.object(sys, 'argv', test_args):
        main()


class TestNoOptions:
    def setUp(self):
        self.config_file = '.moban.yaml'
        copyfile(os.path.join("tests", "fixtures", self.config_file),
                 self.config_file)
        self.data_file = 'data.yaml'
        with open(self.data_file,'w')as f:
            f.write("hello: world")
    
    @patch("moban.template.do_template")
    def test_single_command(self, fake_template_doer):
        test_args = ["moban"]
        with patch.object(sys, 'argv', test_args):
            main()
            fake_template_doer.assert_called_with(
                ['commons/templates', '.moban.d'],
                dict(hello="world"),
                [('README.rst', 'README.rst'), ('setup.py', 'setup.py')]
            )

    def tearDown(self):
        os.unlink(self.config_file)
        os.unlink(self.data_file)


class TestInvalidMobanFile:
    def setUp(self):
        self.config_file = '.moban.yaml'

    @raises(SystemExit)
    @patch("moban.template.do_template")
    def test_no_configuration(self, fake_template_doer):
        with open(self.config_file,'w')as f:
            f.write("")
        test_args = ["moban"]
        with patch.object(sys, 'argv', test_args):
            main()

    @raises(SystemExit)
    @patch("moban.template.do_template")
    def test_no_configuration_2(self, fake_template_doer):
        with open(self.config_file,'w')as f:
            f.write("not: related")
        test_args = ["moban"]
        with patch.object(sys, 'argv', test_args):
            main()

    @raises(SystemExit)
    @patch("moban.template.do_template")
    def test_no_targets(self, fake_template_doer):
        with open(self.config_file,'w')as f:
            f.write("configuration: test")
        test_args = ["moban"]
        with patch.object(sys, 'argv', test_args):
            main()

    def tearDown(self):
        os.unlink(self.config_file)
