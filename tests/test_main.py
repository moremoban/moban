import os
import sys
from shutil import copyfile
from nose.tools import raises
from mock import patch
import moban.exceptions as exceptions


class TestException:
    def setUp(self):
        self.moban_file = '.moban.yml'
        self.data_file = 'data.yml'

    def tearDown(self):
        if os.path.exists(self.moban_file):
            os.unlink(self.moban_file)
        if os.path.exists(self.data_file):
            os.unlink(self.data_file)
        if os.path.exists('.moban.hashes'):
            os.unlink('.moban.hashes')

    @raises(exceptions.MobanfileGrammarException)
    def test_handle_moban_file(self):
        copyfile(os.path.join("tests", "fixtures", ".moban-version-1234.yml"),
                 self.moban_file)
        import moban.main as main
        main.handle_moban_file({})

    @raises(exceptions.MobanfileGrammarException)
    def test_version_1_is_recognized(self):
        copyfile(os.path.join("tests", "fixtures", ".moban-version-1.0.yml"),
                 self.moban_file)
        copyfile(os.path.join("tests", "fixtures", ".moban-version-1.0.yml"),
                 self.data_file)
        import moban.main as main
        main.handle_moban_file({})

    @patch('os.path.exists')
    @patch('moban.main.handle_moban_file')
    @patch('moban.reporter.report_error_message')
    def test_directory_not_found(self,
                                 fake_reporter, fake_moban_file, fake_file):
        fake_file.return_value = True
        fake_moban_file.side_effect = exceptions.DirectoryNotFound
        from moban.main import main
        with patch.object(sys, 'argv', ['moban']):
            main()
        assert fake_reporter.called

    @patch('os.path.exists')
    @patch('moban.main.handle_moban_file')
    @patch('moban.reporter.report_error_message')
    def test_no_third_party_engine(self,
                                   fake_reporter, fake_moban_file, fake_file):
        fake_file.return_value = True
        fake_moban_file.side_effect = exceptions.NoThirdPartyEngine
        from moban.main import main
        with patch.object(sys, 'argv', ['moban']):
            main()
        assert fake_reporter.called
