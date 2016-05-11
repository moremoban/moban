import os
import sys
from shutil import copyfile
from moban.main import main
from mock import patch
from nose.tools import raises, assert_raises


class TestCustomOptions:
    def setUp(self):
        self.config_file = 'config.yaml'
        with open(self.config_file,'w')as f:
            f.write("hello: world")
    
    @patch("moban.engine.Engine.render_to_file")
    def test_custom_options(self, fake_template_doer):
        test_args = ["moban", "-c", self.config_file,
                     "-cd", "/home/developer/configuration",
                     "-td", "/home/developer/templates",
                     "-t", "a.template"]
        with patch.object(sys, 'argv', test_args):
            main()
            fake_template_doer.assert_called_with(
                'a.template', 'config.yaml', 'moban.output'
            )
    
    @patch("moban.engine.Engine.render_to_file")
    def test_minimal_options(self, fake_template_doer):
        test_args = ["moban", "-c", self.config_file,
                     "-t", "a.template"]
        with patch.object(sys, 'argv', test_args):
            main()
            fake_template_doer.assert_called_with(
                'a.template', 'config.yaml', 'moban.output'
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
        self.config_file = 'data.yml'
        with open(self.config_file,'w')as f:
            f.write("hello: world")
    
    @patch("moban.engine.Engine.render_to_file")
    def test_default_options(self, fake_template_doer):
        test_args = ["moban", "-t", "a.template"]
        with patch.object(sys, 'argv', test_args):
            main()
            fake_template_doer.assert_called_with(
                'a.template', 'data.yml', 'moban.output'
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
        self.config_file = '.moban.yml'
        copyfile(os.path.join("tests", "fixtures", self.config_file),
                 self.config_file)
        self.data_file = 'data.yaml'
        with open(self.data_file,'w')as f:
            f.write("hello: world")
    
    @patch("moban.engine.Engine.render_to_files")
    def test_single_command(self, fake_template_doer):
        test_args = ["moban"]
        with patch.object(sys, 'argv', test_args):
            main()
            call_args = list(fake_template_doer.call_args[0][0])
            assert call_args == [
                ('README.rst', 'data.yaml', 'README.rst'),
                ('setup.py', 'data.yaml', 'setup.py')]

    def tearDown(self):
        os.unlink(self.config_file)
        os.unlink(self.data_file)


class TestNoOptions:
    def setUp(self):
        self.config_file = '.moban.yml'
        copyfile(os.path.join("tests", "fixtures", self.config_file),
                 self.config_file)
        self.data_file = 'data.yaml'
        with open(self.data_file,'w')as f:
            f.write("hello: world")
    
    @patch("moban.engine.Engine.render_to_files")
    def test_single_command(self, fake_template_doer):
        test_args = ["moban"]
        with patch.object(sys, 'argv', test_args):
            main()
            call_args = list(fake_template_doer.call_args[0][0])
            assert call_args == [
                ('README.rst', 'data.yaml', 'README.rst'),
                ('setup.py', 'data.yaml', 'setup.py')]

    def tearDown(self):
        os.unlink(self.config_file)
        os.unlink(self.data_file)


def test_duplicated_targets_in_moban_file():
    config_file = 'duplicated.moban.yml'
    copyfile(os.path.join("tests", "fixtures", config_file),
             '.moban.yml')
    test_args = ["moban"]
    with patch.object(sys, 'argv', test_args):
        assert_raises(SyntaxError, main)
    os.unlink('.moban.yml')


class TestInvalidMobanFile:
    def setUp(self):
        self.config_file = '.moban.yml'

    @raises(SystemExit)
    @patch("moban.engine.Engine.render_to_files")
    def test_no_configuration(self, fake_template_doer):
        with open(self.config_file,'w')as f:
            f.write("")
        test_args = ["moban"]
        with patch.object(sys, 'argv', test_args):
            main()

    @raises(SystemExit)
    @patch("moban.engine.Engine.render_to_files")
    def test_no_configuration_2(self, fake_template_doer):
        with open(self.config_file,'w')as f:
            f.write("not: related")
        test_args = ["moban"]
        with patch.object(sys, 'argv', test_args):
            main()

    @raises(SystemExit)
    @patch("moban.engine.Engine.render_to_files")
    def test_no_targets(self, fake_template_doer):
        with open(self.config_file,'w')as f:
            f.write("configuration: test")
        test_args = ["moban"]
        with patch.object(sys, 'argv', test_args):
            main()

    def tearDown(self):
        os.unlink(self.config_file)


class TestComplexOptions:
    def setUp(self):
        self.config_file = '.moban.yml'
        copyfile(os.path.join("tests", "fixtures", ".moban-2.yml"),
                 self.config_file)
        self.data_file = 'data.yaml'
        with open(self.data_file,'w')as f:
            f.write("hello: world")
    
    @patch("moban.engine.Engine.render_to_files")
    def test_single_command(self, fake_template_doer):
        test_args = ["moban"]
        with patch.object(sys, 'argv', test_args):
            main()
            call_args = list(fake_template_doer.call_args[0][0])
            assert call_args == [
                ('README.rst', 'custom-data.yaml', 'README.rst'),
                ('setup.py', 'data.yml', 'setup.py')]

    def tearDown(self):
        os.unlink(self.config_file)
        os.unlink(self.data_file)



class TestTemplateTypeOption:
    def setUp(self):
        self.config_file = 'data.yml'
        with open(self.config_file,'w')as f:
            f.write("hello: world")
    
    @patch("moban.engine.Engine.render_to_file")
    def test_mako_optoin(self, fake_template_doer):
        test_args = ["moban", "-t", "a.template", "--template_type", "mako"]
        with patch.object(sys, 'argv', test_args):
            main()
            fake_template_doer.assert_called_with(
                'a.template', 'data.yml', 'moban.output'
            )

    def tearDown(self):
        os.unlink(self.config_file)


