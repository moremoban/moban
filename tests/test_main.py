import os
from shutil import copyfile
from nose.tools import raises


class TestException:
    def setUp(self):
        self.moban_file = '.moban.yml'
        self.data_file = 'data.yml'

    def tearDown(self):
        os.unlink(self.moban_file)
        if os.path.exists(self.data_file):
            os.unlink(self.data_file)

    @raises(NotImplementedError)
    def test_vhandle_moban_file(self):
        copyfile(os.path.join("tests", "fixtures", ".moban-version-1234.yml"),
                 self.moban_file)
        import moban.main as main
        main.handle_moban_file({})

    @raises(SystemExit)
    def test_version_1_is_recognized(self):
        copyfile(os.path.join("tests", "fixtures", ".moban-version-1.0.yml"),
                 self.moban_file)
        copyfile(os.path.join("tests", "fixtures", ".moban-version-1.0.yml"),
                 self.data_file)
        import moban.main as main
        main.handle_moban_file({})
