import os
import sys
from shutil import copyfile

from mock import MagicMock, patch
from nose.tools import eq_, raises, assert_raises

import moban.exceptions as exceptions


class TestException:
    def setUp(self):
        self.moban_file = ".moban.yml"
        self.data_file = "data.yml"

    def tearDown(self):
        if os.path.exists(self.moban_file):
            os.unlink(self.moban_file)
        if os.path.exists(self.data_file):
            os.unlink(self.data_file)

    @raises(exceptions.MobanfileGrammarException)
    def test_handle_moban_file(self):
        copyfile(
            os.path.join("tests", "fixtures", ".moban-version-1234.yml"),
            self.moban_file,
        )
        import moban.main as main

        main.handle_moban_file(self.moban_file, {})

    def test_check_none(self):
        import moban.main as main
        from ruamel.yaml import YAML

        yaml = YAML()

        invalid_data = [
            """targets:
              - output:""",
            """configuration:
              template_dir:
                - cool-templates
                -""",
        ]

        valid_data = [
            """targets:
              - output: template""",
            """configuration:
              template_dir:
                - cool-templates
                - custom-templates""",
        ]

        for data in (yaml.load(d) for d in invalid_data):
            assert_raises(
                exceptions.MobanfileGrammarException,
                main.check_none,
                data,
                ".moban.yaml",
            )

        for data in (yaml.load(d) for d in valid_data):
            main.check_none(data, ".moban.yaml")

    @raises(exceptions.MobanfileGrammarException)
    def test_version_1_is_recognized(self):
        copyfile(
            os.path.join("tests", "fixtures", ".moban-version-1.0.yml"),
            self.moban_file,
        )
        copyfile(
            os.path.join("tests", "fixtures", ".moban-version-1.0.yml"),
            self.data_file,
        )
        import moban.main as main

        main.handle_moban_file(self.moban_file, {})

    @raises(SystemExit)
    @patch("os.path.exists")
    @patch("moban.main.handle_moban_file")
    @patch("moban.externals.reporter.report_error_message")
    def test_directory_not_found(
        self, fake_reporter, fake_moban_file, fake_file
    ):
        fake_file.return_value = True
        fake_moban_file.side_effect = exceptions.DirectoryNotFound
        fake_stdin = MagicMock(isatty=MagicMock(return_value=True))
        with patch.object(sys, "stdin", fake_stdin):
            with patch.object(sys, "argv", ["moban"]):
                from moban.main import main

                main()

    @raises(SystemExit)
    @patch("os.path.exists")
    @patch("moban.main.handle_moban_file")
    @patch("moban.externals.reporter.report_error_message")
    def test_unknown_protocol(self, fake_reporter, fake_moban_file, fake_file):
        fake_file.return_value = True
        fake_moban_file.side_effect = exceptions.UnsupportedPyFS2Protocol
        fake_stdin = MagicMock(isatty=MagicMock(return_value=True))
        with patch.object(sys, "stdin", fake_stdin):
            from moban.main import main

            with patch.object(sys, "argv", ["moban"]):
                main()

    @raises(SystemExit)
    @patch("os.path.exists")
    @patch("moban.main.handle_command_line")
    @patch("moban.externals.reporter.report_error_message")
    def test_unknown_protocol_at_command_line(
        self, fake_reporter, fake_moban_file, fake_file
    ):
        fake_file.return_value = False
        fake_moban_file.side_effect = exceptions.UnsupportedPyFS2Protocol
        fake_stdin = MagicMock(isatty=MagicMock(return_value=True))
        with patch.object(sys, "stdin", fake_stdin):
            from moban.main import main

            with patch.object(sys, "argv", ["moban"]):
                main()

    @raises(SystemExit)
    @patch("os.path.exists")
    @patch("moban.main.handle_moban_file")
    @patch("moban.externals.reporter.report_error_message")
    def test_no_third_party_engine(
        self, fake_reporter, fake_moban_file, fake_file
    ):
        fake_file.return_value = True
        fake_moban_file.side_effect = exceptions.NoThirdPartyEngine
        fake_stdin = MagicMock(isatty=MagicMock(return_value=True))
        with patch.object(sys, "stdin", fake_stdin):
            from moban.main import main

            with patch.object(sys, "argv", ["moban"]):
                main()

    @raises(SystemExit)
    @patch("os.path.exists")
    @patch("moban.main.handle_moban_file")
    @patch("moban.externals.reporter.report_error_message")
    def test_double_underscore_main(
        self, fake_reporter, fake_moban_file, fake_file
    ):
        fake_file.return_value = True
        fake_moban_file.side_effect = exceptions.DirectoryNotFound
        fake_stdin = MagicMock(isatty=MagicMock(return_value=True))
        with patch.object(sys, "stdin", fake_stdin):
            from moban.__main__ import main

            with patch.object(sys, "argv", ["moban"]):
                main()


class TestExitCodes:
    @raises(SystemExit)
    @patch("moban.main.handle_moban_file")
    @patch("moban.main.find_default_moban_file")
    def test_has_many_files_with_exit_code(
        self, fake_find_file, fake_moban_file
    ):
        fake_find_file.return_value = "abc"
        fake_moban_file.return_value = 1
        from moban.main import main

        with patch.object(sys, "argv", ["moban", "--exit-code"]):
            main()

    @raises(SystemExit)
    @patch("moban.main.handle_command_line")
    @patch("moban.main.find_default_moban_file")
    def test_handle_single_change_with_exit_code(
        self, fake_find_file, fake_command_line
    ):
        fake_find_file.return_value = None
        fake_command_line.return_value = 1
        from moban.main import main

        with patch.object(sys, "argv", ["moban", "--exit-code"]):
            main()

    @patch("moban.main.handle_moban_file")
    @patch("moban.main.find_default_moban_file")
    def test_has_many_files(self, fake_find_file, fake_moban_file):
        fake_find_file.return_value = "abc"
        fake_moban_file.return_value = 1
        from moban.main import main

        with patch.object(sys, "argv", ["moban"]):
            main()

    @patch("moban.main.handle_command_line")
    @patch("moban.main.find_default_moban_file")
    def test_handle_single_change(self, fake_find_file, fake_command_line):
        fake_find_file.return_value = None
        fake_command_line.return_value = 1
        from moban.main import main

        with patch.object(sys, "argv", ["moban"]):
            main()


class TestFinder:
    def setUp(self):
        self.patcher = patch("moban.externals.file_system.exists")
        self.fake_file_existence = self.patcher.start()
        self.fake_file_existence.__name__ = "fake"
        self.fake_file_existence.__module__ = "fake"

    def tearDown(self):
        self.patcher.stop()

    def test_moban_yml(self):
        self.fake_file_existence.return_value = True
        from moban.main import find_default_moban_file

        actual = find_default_moban_file()
        eq_(".moban.yml", actual)

    def test_moban_yaml(self):
        self.fake_file_existence.side_effect = [False, True]
        from moban.main import find_default_moban_file

        actual = find_default_moban_file()
        eq_(".moban.yaml", actual)

    def test_no_moban_file(self):
        self.fake_file_existence.side_effect = [False, False]
        from moban.main import find_default_moban_file

        actual = find_default_moban_file()
        assert actual is None
