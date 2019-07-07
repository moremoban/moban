import os
import sys
from shutil import copyfile

from mock import patch
from nose.tools import eq_, raises, assert_raises
from moban.definitions import TemplateTarget


class TestCustomOptions:
    def setUp(self):
        self.config_file = "config.yaml"
        with open(self.config_file, "w") as f:
            f.write("hello: world")
        self.patcher1 = patch(
            "moban.utils.verify_the_existence_of_directories"
        )
        self.patcher1.start()

    @patch("moban.plugins.template.MobanEngine.render_to_file")
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

    @patch("moban.plugins.template.MobanEngine.render_to_file")
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
            "moban.utils.verify_the_existence_of_directories"
        )
        self.patcher1.start()

    @patch("moban.plugins.template.MobanEngine.render_to_file")
    def test_default_options(self, fake_template_doer):
        test_args = ["moban", "-t", "a.jj2"]
        with patch.object(sys, "argv", test_args):
            from moban.main import main

            main()
            fake_template_doer.assert_called_with(
                "a.jj2", "data.yml", "moban.output"
            )

    @patch("moban.plugins.template.MobanEngine.render_string_to_file")
    def test_string_template(self, fake_template_doer):
        string_template = "{{HELLO}}"
        test_args = ["moban", string_template]
        with patch.object(sys, "argv", test_args):
            from moban.main import main

            main()
            fake_template_doer.assert_called_with(
                string_template, "data.yml", "moban.output"
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


@raises(Exception)
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
            "moban.utils.verify_the_existence_of_directories"
        )
        self.patcher1.start()

    @patch("moban.plugins.template.MobanEngine.render_to_files")
    def test_single_command(self, fake_template_doer):
        test_args = ["moban"]
        with patch.object(sys, "argv", test_args):
            from moban.main import main

            main()
            call_args = list(fake_template_doer.call_args[0][0])
            eq_(
                call_args,
                [
                    TemplateTarget(
                        "README.rst.jj2", "data.yaml", "README.rst"
                    ),
                    TemplateTarget("setup.py.jj2", "data.yaml", "setup.py"),
                ],
            )

    @raises(Exception)
    @patch("moban.plugins.template.MobanEngine.render_to_files")
    def test_single_command_with_missing_output(self, fake_template_doer):
        test_args = ["moban", "-t", "README.rst.jj2"]
        with patch.object(sys, "argv", test_args):
            from moban.main import main

            main()

    @patch("moban.plugins.template.MobanEngine.render_to_files")
    def test_single_command_with_a_few_options(self, fake_template_doer):
        test_args = ["moban", "-t", "README.rst.jj2", "-o", "xyz.output"]
        with patch.object(sys, "argv", test_args):
            from moban.main import main

            main()
            call_args = list(fake_template_doer.call_args[0][0])
            eq_(
                call_args,
                [TemplateTarget("README.rst.jj2", "data.yaml", "xyz.output")],
            )

    @patch("moban.plugins.template.MobanEngine.render_to_files")
    def test_single_command_with_options(self, fake_template_doer):
        test_args = [
            "moban",
            "-t",
            "README.rst.jj2",
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
                [TemplateTarget("README.rst.jj2", "new.yml", "xyz.output")],
            )

    @raises(Exception)
    def test_single_command_without_output_option(self):
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
            "moban.utils.verify_the_existence_of_directories"
        )
        self.patcher1.start()

    @patch("moban.plugins.template.MobanEngine.render_to_files")
    def test_single_command(self, fake_template_doer):
        test_args = ["moban"]
        with patch.object(sys, "argv", test_args):
            from moban.main import main

            main()
            call_args = list(fake_template_doer.call_args[0][0])
            eq_(
                call_args,
                [
                    TemplateTarget(
                        "README.rst.jj2", "data.yaml", "README.rst"
                    ),
                    TemplateTarget("setup.py.jj2", "data.yaml", "setup.py"),
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
            "moban.utils.verify_the_existence_of_directories"
        )
        self.patcher1.start()

    @patch("moban.plugins.template.MobanEngine.render_to_files")
    def test_single_command(self, fake_template_doer):
        test_args = ["moban", "-m", self.config_file]
        with patch.object(sys, "argv", test_args):
            from moban.main import main

            main()
            call_args = list(fake_template_doer.call_args[0][0])
            eq_(
                call_args,
                [
                    TemplateTarget(
                        "README.rst.jj2", "data.yaml", "README.rst"
                    ),
                    TemplateTarget("setup.py.jj2", "data.yaml", "setup.py"),
                ],
            )

    def tearDown(self):
        self.patcher1.stop()
        os.unlink(self.config_file)
        os.unlink(self.data_file)


class TestTemplateOption:
    def setUp(self):
        self.config_file = "custom-moban.txt"
        copyfile(
            os.path.join("tests", "fixtures", ".moban.yml"), self.config_file
        )
        self.patcher1 = patch(
            "moban.utils.verify_the_existence_of_directories"
        )
        self.patcher1.start()

    @patch("moban.plugins.template.MobanEngine.render_to_file")
    def test_template_option_override_moban_file(self, fake_template_doer):
        test_args = ["moban", "-t", "setup.py.jj2"]
        with patch.object(sys, "argv", test_args):
            from moban.main import main

            main()
            fake_template_doer.assert_called_with(
                "setup.py.jj2", "data.yml", "moban.output"
            )

    @patch("moban.plugins.template.MobanEngine.render_to_file")
    def test_template_option_not_in_moban_file(self, fake_template_doer):
        test_args = ["moban", "-t", "foo.jj2"]
        with patch.object(sys, "argv", test_args):
            from moban.main import main

            main()
            fake_template_doer.assert_called_with(
                "foo.jj2", "data.yml", "moban.output"
            )

    def tearDown(self):
        self.patcher1.stop()
        os.unlink(self.config_file)


@patch("moban.utils.verify_the_existence_of_directories")
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
    @patch("moban.plugins.template.MobanEngine.render_to_files")
    def test_no_configuration(self, fake_template_doer):
        with open(self.config_file, "w") as f:
            f.write("")
        test_args = ["moban"]
        with patch.object(sys, "argv", test_args):
            from moban.main import main

            main()

    @raises(SystemExit)
    @patch("moban.plugins.template.MobanEngine.render_to_files")
    def test_no_configuration_2(self, fake_template_doer):
        with open(self.config_file, "w") as f:
            f.write("not: related")
        test_args = ["moban"]
        with patch.object(sys, "argv", test_args):
            from moban.main import main

            main()

    @raises(SystemExit)
    @patch("moban.plugins.template.MobanEngine.render_to_files")
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

    @patch(
        "moban.utils.verify_the_existence_of_directories", return_value=True
    )
    def test_single_command(self, _):
        test_args = ["moban"]
        with patch.object(sys, "argv", test_args):
            from moban.main import main

            with patch(
                "moban.plugins.template.MobanEngine.render_to_files"
            ) as fake:
                main()
                call_args = list(fake.call_args[0][0])
                eq_(
                    call_args,
                    [
                        TemplateTarget(
                            "README.rst.jj2", "custom-data.yaml", "README.rst"
                        ),
                        TemplateTarget("setup.py.jj2", "data.yml", "setup.py"),
                    ],
                )

    def tearDown(self):
        os.unlink(self.config_file)
        os.unlink(self.data_file)


class TestTemplateTypeOption:
    def setUp(self):
        self.config_file = "data.yml"
        with open(self.config_file, "w") as f:
            f.write("hello: world")

    @patch("moban.plugins.template.MobanEngine.render_to_file")
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


@raises(SystemExit)
def test_version_option():
    test_args = ["moban", "-v"]
    with patch.object(sys, "argv", test_args):
        from moban.main import main

        main()
