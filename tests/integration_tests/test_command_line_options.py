import os
import sys
from shutil import copyfile

from mock import MagicMock, patch
from nose import SkipTest
from nose.tools import eq_, raises, assert_raises

from moban.core.definitions import TemplateTarget

try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO


class TestCustomOptions:
    def setUp(self):
        self.config_file = "config.yaml"
        with open(self.config_file, "w") as f:
            f.write("hello: world")
        self.patcher1 = patch(
            "moban.core.utils.verify_the_existence_of_directories"
        )
        self.patcher1.start()

    @patch("moban.externals.file_system.abspath")
    @patch("moban.core.moban_factory.MobanEngine.render_to_file")
    def test_custom_options(self, fake_template_doer, fake_abspath):
        test_args = [
            "moban",
            "-c",
            self.config_file,
            "-cd",
            ".",
            "-td",
            ".",
            "-t",
            "a.jj2",
        ]
        with patch.object(sys, "argv", test_args):
            from moban.main import main

            main()
            fake_template_doer.assert_called_with(
                "a.jj2", "config.yaml", "moban.output"
            )

    @patch("moban.core.moban_factory.MobanEngine.render_to_file")
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
        fake_stdin = MagicMock(isatty=MagicMock(return_value=True))
        with patch.object(sys, "stdin", fake_stdin):
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
            "moban.core.utils.verify_the_existence_of_directories"
        )
        self.patcher1.start()

    @patch("moban.core.moban_factory.MobanEngine.render_to_file")
    def test_default_options(self, fake_template_doer):
        test_args = ["moban", "-t", "a.jj2"]
        with patch.object(sys, "argv", test_args):
            from moban.main import main

            main()
            fake_template_doer.assert_called_with(
                "a.jj2", "data.yml", "moban.output"
            )

    @patch("moban.core.moban_factory.MobanEngine.render_string_to_file")
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
        fake_stdin = MagicMock(isatty=MagicMock(return_value=True))
        with patch.object(sys, "stdin", fake_stdin):
            with patch.object(sys, "argv", test_args):
                from moban.main import main

                main()

    def tearDown(self):
        self.patcher1.stop()
        os.unlink(self.config_file)


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
            "moban.core.utils.verify_the_existence_of_directories"
        )
        self.patcher1.start()

    @patch("moban.core.moban_factory.MobanEngine.render_to_files")
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
    @patch("moban.core.moban_factory.MobanEngine.render_to_files")
    def test_single_command_with_missing_output(self, fake_template_doer):
        test_args = ["moban", "-t", "README.rst.jj2"]
        with patch.object(sys, "argv", test_args):
            from moban.main import main

            main()

    @patch("moban.core.moban_factory.MobanEngine.render_to_files")
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

    @patch("moban.core.moban_factory.MobanEngine.render_to_files")
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
            "moban.core.utils.verify_the_existence_of_directories"
        )
        self.patcher1.start()

    @patch("moban.core.moban_factory.MobanEngine.render_to_files")
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
            "moban.core.utils.verify_the_existence_of_directories"
        )
        self.patcher1.start()

    @patch("moban.core.moban_factory.MobanEngine.render_to_files")
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
            "moban.core.utils.verify_the_existence_of_directories"
        )
        self.patcher1.start()

    @patch("moban.core.moban_factory.MobanEngine.render_to_file")
    def test_template_option_override_moban_file(self, fake_template_doer):
        test_args = ["moban", "-t", "setup.py.jj2"]
        with patch.object(sys, "argv", test_args):
            from moban.main import main

            main()
            fake_template_doer.assert_called_with(
                "setup.py.jj2", "data.yml", "moban.output"
            )

    @patch("moban.core.moban_factory.MobanEngine.render_to_file")
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


@patch("moban.core.utils.verify_the_existence_of_directories")
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
    @patch("moban.core.moban_factory.MobanEngine.render_to_files")
    def test_no_configuration(self, fake_template_doer):
        with open(self.config_file, "w") as f:
            f.write("")
        test_args = ["moban"]
        with patch.object(sys, "argv", test_args):
            from moban.main import main

            main()

    @raises(SystemExit)
    @patch("moban.core.moban_factory.MobanEngine.render_to_files")
    def test_no_configuration_2(self, fake_template_doer):
        with open(self.config_file, "w") as f:
            f.write("not: related")
        test_args = ["moban"]
        with patch.object(sys, "argv", test_args):
            from moban.main import main

            main()

    @raises(SystemExit)
    @patch("moban.core.moban_factory.MobanEngine.render_to_files")
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
        "moban.core.utils.verify_the_existence_of_directories",
        return_value=".",
    )
    def test_single_command(self, _):
        test_args = ["moban"]
        with patch.object(sys, "argv", test_args):
            from moban.main import main

            with patch(
                "moban.core.moban_factory.MobanEngine.render_to_files"
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

    @patch("moban.core.moban_factory.MobanEngine.render_to_file")
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
    test_args = ["moban", "-V"]
    with patch.object(sys, "argv", test_args):
        from moban.main import main

        main()


@patch("logging.basicConfig")
def test_warning_verbose(fake_config):
    fake_config.side_effect = [IOError("stop test")]
    test_args = ["moban", "-vvv"]
    with patch.object(sys, "argv", test_args):
        from moban.main import main

        try:
            main()
        except IOError:
            fake_config.assert_called_with(
                format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
                level=10,
            )


@patch("logging.basicConfig")
def test_debug_five_verbose_option(fake_config, *_):
    fake_config.side_effect = [IOError("stop test")]
    test_args = ["moban", "-vvvvv"]
    with patch.object(sys, "argv", test_args):
        from moban.main import main

        try:
            main()
        except IOError:
            fake_config.assert_called_with(
                format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
                level=10,
            )


@patch("moban.core.utils.verify_the_existence_of_directories", return_value=[])
def test_git_repo_example(_):
    test_args = [
        "moban",
        "-t",
        "git://github.com/moremoban/pypi-mobans.git!/templates/_version.py.jj2",
        "-c",
        "git://github.com/moremoban/pypi-mobans.git!/config/data.yml",
        "-o",
        "test_git_repo_example.py",
    ]
    with patch.object(sys, "argv", test_args):
        from moban.main import main

        main()
        with open("test_git_repo_example.py") as f:
            content = f.read()
            eq_(content, '__version__ = "0.1.1rc3"\n__author__ = "C.W."\n')
        os.unlink("test_git_repo_example.py")


@patch("moban.core.utils.verify_the_existence_of_directories", return_value=[])
def test_pypi_pkg_example(_):
    test_args = [
        "moban",
        "-t",
        "pypi://pypi-mobans-pkg/resources/templates/_version.py.jj2",
        "-c",
        "pypi://pypi-mobans-pkg/resources/config/data.yml",
        "-o",
        "test_pypi_pkg_example.py",
    ]
    with patch.object(sys, "argv", test_args):
        from moban.main import main

        main()
        with open("test_pypi_pkg_example.py") as f:
            content = f.read()
            eq_(content, '__version__ = "0.1.1rc3"\n__author__ = "C.W."\n')
        os.unlink("test_pypi_pkg_example.py")


def test_add_extension():
    if sys.version_info[0] == 2:
        raise SkipTest("jinja2-python-version does not support python 2")
    test_commands = [
        [
            "moban",
            "-t",
            "{{ python_version }}",
            "-e",
            "jinja2=jinja2_python_version.PythonVersionExtension",
        ],
        [
            "moban",
            "-t",
            "{{ python_version }}",
            "-e",
            "jj2=jinja2_python_version.PythonVersionExtension",
        ],
    ]
    for test_args in test_commands:
        with patch.object(sys, "argv", test_args):
            from moban.main import main

            main()
            with open("moban.output") as f:
                content = f.read()
                eq_(
                    content,
                    "{}.{}".format(sys.version_info[0], sys.version_info[1]),
                )
            os.unlink("moban.output")


def test_stdin_input():
    if sys.platform == "win32":
        raise SkipTest("windows test fails with this pipe test 2")
    test_args = ["moban", "-d", "hello=world"]
    with patch.object(sys, "stdin", StringIO("{{hello}}")):
        with patch.object(sys, "argv", test_args):
            from moban.main import main

            main()
            with open("moban.output") as f:
                content = f.read()
                eq_(content, "world")
            os.unlink("moban.output")
