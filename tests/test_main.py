import os
import sys
from shutil import copyfile

import moban.exceptions as exceptions
from mock import patch
from nose.tools import raises, assert_raises


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
    @patch("moban.reporter.report_error_message")
    def test_directory_not_found(
        self, fake_reporter, fake_moban_file, fake_file
    ):
        fake_file.return_value = True
        fake_moban_file.side_effect = exceptions.DirectoryNotFound
        from moban.main import main

        with patch.object(sys, "argv", ["moban"]):
            main()

    @raises(SystemExit)
    @patch("os.path.exists")
    @patch("moban.main.handle_moban_file")
    @patch("moban.reporter.report_error_message")
    def test_no_third_party_engine(
        self, fake_reporter, fake_moban_file, fake_file
    ):
        fake_file.return_value = True
        fake_moban_file.side_effect = exceptions.NoThirdPartyEngine
        from moban.main import main

        with patch.object(sys, "argv", ["moban"]):
            main()

    @raises(SystemExit)
    @patch("os.path.exists")
    @patch("moban.main.handle_moban_file")
    @patch("moban.reporter.report_error_message")
    def test_double_underscore_main(
        self, fake_reporter, fake_moban_file, fake_file
    ):
        fake_file.return_value = True
        fake_moban_file.side_effect = exceptions.DirectoryNotFound
        from moban.__main__ import main

        with patch.object(sys, "argv", ["moban"]):
            main()


class TestExitCodes:
    @raises(SystemExit)
    @patch("moban.main.handle_moban_file")
    @patch("moban.mobanfile.find_default_moban_file")
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
    @patch("moban.mobanfile.find_default_moban_file")
    def test_handle_single_change_with_exit_code(
        self, fake_find_file, fake_command_line
    ):
        fake_find_file.return_value = None
        fake_command_line.return_value = 1
        from moban.main import main

        with patch.object(sys, "argv", ["moban", "--exit-code"]):
            main()

    @patch("moban.main.handle_moban_file")
    @patch("moban.mobanfile.find_default_moban_file")
    def test_has_many_files(self, fake_find_file, fake_moban_file):
        fake_find_file.return_value = "abc"
        fake_moban_file.return_value = 1
        from moban.main import main

        with patch.object(sys, "argv", ["moban"]):
            main()

    @patch("moban.main.handle_command_line")
    @patch("moban.mobanfile.find_default_moban_file")
    def test_handle_single_change(self, fake_find_file, fake_command_line):
        fake_find_file.return_value = None
        fake_command_line.return_value = 1
        from moban.main import main

        with patch.object(sys, "argv", ["moban"]):
            main()
