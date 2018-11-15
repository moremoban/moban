import os
import sys
from shutil import copyfile

from mock import patch
from nose.tools import eq_, raises, assert_raises


class TestCustomOptions:
    def setUp(self):
        self.config_file = "config.yaml"
        with open(self.config_file, "w") as f:
            f.write("hello: world")
        self.patcher1 = patch(
            "moban.plugins.verify_the_existence_of_directories"
        )
        self.patcher1.start()

    @patch("moban.jinja2.engine.Engine.render_to_file")
    def test_custom_options(self, fake_template_doer):
        test_args = [
            "moban",
            "-c",
            self.config_file,
            "-cd",
            "/home/developer/configuration",
            "-td",
            "/home/developer/templates",
            "-t",
            "a.jj2",
        ]
        with patch.object(sys, "argv", test_args):
            from moban.main import main

            main()
            fake_template_doer.assert_called_with(
                "a.jj2", "config.yaml", "moban.output"
            )

    @patch("moban.jinja2.engine.Engine.render_to_file")
    def test_minimal_options(self, fake_template_doer):
        test_args = ["moban", "-c", self.config_file, "-t", "a.jj2"]
        with patch.object(sys, "argv", test_args):
            from moban.main import main

            main()
            fake_template_doer.assert_called_with(
                "a.jj2", "config.yaml", "moban.output"
            )

    @raises(SystemExit)
    def test_missing_template(self):
        test_args = ["moban", "-c", self.config_file]
        with patch.object(sys, "argv", test_args):
            from moban.main import main

            main()

    def tearDown(self):
        self.patcher1.stop()
        os.unlink(self.config_file)


class TestOptions:
    def setUp(self):
        self.config_file = "data.yml"
        with open(self.config_file, "w") as f:
            f.write("hello: world")
        self.patcher1 = patch(
            "moban.plugins.verify_the_existence_of_directories"
        )
        self.patcher1.start()

    @patch("moban.jinja2.engine.Engine.render_to_file")
    def test_default_options(self, fake_template_doer):
        test_args = ["moban", "-t", "a.jj2"]
        with patch.object(sys, "argv", test_args):
            from moban.main import main

            main()
            fake_template_doer.assert_called_with(
                "a.jj2", "data.yml", "moban.output"
            )

    @raises(SystemExit)
    def test_no_argments(self):
        test_args = ["moban"]
        with patch.object(sys, "argv", test_args):
            from moban.main import main

            main()

    def tearDown(self):
        self.patcher1.stop()
        os.unlink(self.config_file)


@raises(IOError)
def test_missing_configuration():
    test_args = ["moban", "-t", "a.jj2"]
    with patch.object(sys, "argv", test_args):
        from moban.main import main

        main()


class TestNoOptions:
    def setUp(self):
        self.config_file = ".moban.yml"
        copyfile(
            os.path.join("tests", "fixtures", self.config_file),
            self.config_file,
        )
        self.data_file = "data.yaml"
        with open(self.data_file, "w") as f:
            f.write("hello: world")
        self.patcher1 = patch(
            "moban.plugins.verify_the_existence_of_directories"
        )
        self.patcher1.start()

    @patch("moban.jinja2.engine.Engine.render_to_files")
    def test_single_command(self, fake_template_doer):
        test_args = ["moban"]
        with patch.object(sys, "argv", test_args):
            from moban.main import main

            main()
            call_args = list(fake_template_doer.call_args[0][0])
            eq_(
                call_args,
                [
                    ("README.rst.jj2", "data.yaml", "README.rst"),
                    ("setup.py.jj2", "data.yaml", "setup.py"),
                ],
            )

    @patch("moban.jinja2.engine.Engine.render_to_files")
    def test_single_command_with_a_few_options(self, fake_template_doer):
        test_args = ["moban", "-t", "abc.jj2", "-o", "xyz.output"]
        with patch.object(sys, "argv", test_args):
            from moban.main import main

            main()
            call_args = list(fake_template_doer.call_args[0][0])
            eq_(
                call_args,
                [
                    ("README.rst.jj2", "data.yaml", "README.rst"),
                    ("setup.py.jj2", "data.yaml", "setup.py"),
                    ("abc.jj2", "data.yaml", "xyz.output"),
                ],
            )

    @patch("moban.jinja2.engine.Engine.render_to_files")
    def test_single_command_with_options(self, fake_template_doer):
        test_args = [
            "moban",
            "-t",
            "abc.jj2",
            "-c",
            "new.yml",
            "-o",
            "xyz.output",
        ]
        with patch.object(sys, "argv", test_args):
            from moban.main import main

            main()
            call_args = list(fake_template_doer.call_args[0][0])
            eq_(
                call_args,
                [
                    ("README.rst.jj2", "new.yml", "README.rst"),
                    ("setup.py.jj2", "new.yml", "setup.py"),
                    ("abc.jj2", "new.yml", "xyz.output"),
                ],
            )

    @raises(Exception)
    @patch("moban.jinja2.engine.Engine.render_to_files")
    def test_single_command_without_output_option(self, fake_template_doer):
        test_args = ["moban", "-t", "abc.jj2"]
        with patch.object(sys, "argv", test_args):
            from moban.main import main

            main()

    def tearDown(self):
        os.unlink(self.config_file)
        os.unlink(self.data_file)
        self.patcher1.stop()


class TestNoOptions2:
    def setUp(self):
        self.config_file = ".moban.yml"
        copyfile(
            os.path.join("tests", "fixtures", self.config_file),
            self.config_file,
        )
        self.data_file = "data.yaml"
        with open(self.data_file, "w") as f:
            f.write("hello: world")
        self.patcher1 = patch(
            "moban.plugins.verify_the_existence_of_directories"
        )
        self.patcher1.start()

    @patch("moban.jinja2.engine.Engine.render_to_files")
    def test_single_command(self, fake_template_doer):
        test_args = ["moban"]
        with patch.object(sys, "argv", test_args):
            from moban.main import main

            main()
            call_args = list(fake_template_doer.call_args[0][0])
            eq_(
                call_args,
                [
                    ("README.rst.jj2", "data.yaml", "README.rst"),
                    ("setup.py.jj2", "data.yaml", "setup.py"),
                ],
            )

    def tearDown(self):
        self.patcher1.stop()
        os.unlink(self.config_file)
        os.unlink(self.data_file)


class TestCustomMobanFile:
    def setUp(self):
        self.config_file = "custom-moban.txt"
        copyfile(
            os.path.join("tests", "fixtures", ".moban.yml"), self.config_file
        )
        self.data_file = "data.yaml"
        with open(self.data_file, "w") as f:
            f.write("hello: world")
        self.patcher1 = patch(
            "moban.plugins.verify_the_existence_of_directories"
        )
        self.patcher1.start()

    @patch("moban.jinja2.engine.Engine.render_to_files")
    def test_single_command(self, fake_template_doer):
        test_args = ["moban", "-m", self.config_file]
        with patch.object(sys, "argv", test_args):
            from moban.main import main

            main()
            call_args = list(fake_template_doer.call_args[0][0])
            eq_(
                call_args,
                [
                    ("README.rst.jj2", "data.yaml", "README.rst"),
                    ("setup.py.jj2", "data.yaml", "setup.py"),
                ],
            )

    def tearDown(self):
        self.patcher1.stop()
        os.unlink(self.config_file)
        os.unlink(self.data_file)


@patch("moban.plugins.verify_the_existence_of_directories")
def test_duplicated_targets_in_moban_file(fake_verify):
    config_file = "duplicated.moban.yml"
    copyfile(os.path.join("tests", "fixtures", config_file), ".moban.yml")
    test_args = ["moban"]
    with patch.object(sys, "argv", test_args):
        from moban.main import main

        assert_raises(SystemExit, main)
    os.unlink(".moban.yml")


class TestInvalidMobanFile:
    def setUp(self):
        self.config_file = ".moban.yml"

    @raises(SystemExit)
    @patch("moban.jinja2.engine.Engine.render_to_files")
    def test_no_configuration(self, fake_template_doer):
        with open(self.config_file, "w") as f:
            f.write("")
        test_args = ["moban"]
        with patch.object(sys, "argv", test_args):
            from moban.main import main

            main()

    @raises(SystemExit)
    @patch("moban.jinja2.engine.Engine.render_to_files")
    def test_no_configuration_2(self, fake_template_doer):
        with open(self.config_file, "w") as f:
            f.write("not: related")
        test_args = ["moban"]
        with patch.object(sys, "argv", test_args):
            from moban.main import main

            main()

    @raises(SystemExit)
    @patch("moban.jinja2.engine.Engine.render_to_files")
    def test_no_targets(self, fake_template_doer):
        with open(self.config_file, "w") as f:
            f.write("configuration: test")
        test_args = ["moban"]
        with patch.object(sys, "argv", test_args):
            from moban.main import main

            main()

    def tearDown(self):
        os.unlink(self.config_file)


class TestComplexOptions:
    def setUp(self):
        self.config_file = ".moban.yml"
        copyfile(
            os.path.join("tests", "fixtures", ".moban-2.yml"), self.config_file
        )
        self.data_file = "data.yaml"
        with open(self.data_file, "w") as f:
            f.write("hello: world")
        self.patcher1 = patch(
            "moban.plugins.verify_the_existence_of_directories"
        )
        self.patcher1.start()

    def test_single_command(self):
        test_args = ["moban"]
        with patch.object(sys, "argv", test_args):
            from moban.main import main

            with patch("moban.jinja2.engine.Engine.render_to_files") as fake:
                main()
                call_args = list(fake.call_args[0][0])
                eq_(
                    call_args,
                    [
                        ("README.rst.jj2", "custom-data.yaml", "README.rst"),
                        ("setup.py.jj2", "data.yml", "setup.py"),
                    ],
                )

    def tearDown(self):
        os.unlink(self.config_file)
        os.unlink(self.data_file)
        self.patcher1.stop()


class TestTemplateTypeOption:
    def setUp(self):
        self.config_file = "data.yml"
        with open(self.config_file, "w") as f:
            f.write("hello: world")

    @patch("moban.jinja2.engine.Engine.render_to_file")
    def test_mako_option(self, fake_template_doer):
        test_args = ["moban", "-t", "a.mako"]
        with patch.object(sys, "argv", test_args):
            from moban.main import main

            main()
            fake_template_doer.assert_called_with(
                "a.mako", "data.yml", "moban.output"
            )

    def tearDown(self):
        os.unlink(self.config_file)
