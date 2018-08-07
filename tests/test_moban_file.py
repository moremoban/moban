from nose.tools import eq_
from mock import patch


class TestFinder:
    def setUp(self):
        self.patcher = patch("os.path.exists")
        self.fake_file_existence = self.patcher.start()
        self.fake_file_existence.__name__ = "fake"
        self.fake_file_existence.__module__ = "fake"

    def tearDown(self):
        self.patcher.stop()

    def test_moban_yml(self):
        self.fake_file_existence.return_value = True
        from moban.mobanfile import find_default_moban_file

        actual = find_default_moban_file()
        eq_(".moban.yml", actual)

    def test_moban_yaml(self):
        self.fake_file_existence.side_effect = [False, True]
        from moban.mobanfile import find_default_moban_file

        actual = find_default_moban_file()
        eq_(".moban.yaml", actual)

    def test_no_moban_file(self):
        self.fake_file_existence.side_effect = [False, False]
        from moban.mobanfile import find_default_moban_file

        actual = find_default_moban_file()
        assert actual is None


@patch("moban.mobanfile.pip_install")
def test_handle_requires(fake_pip_install):
    modules = ["package1", "package2"]
    from moban.mobanfile import handle_requires

    handle_requires(modules)
    fake_pip_install.assert_called_with(modules)
