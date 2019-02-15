from mock import patch
from nose.tools import eq_

from moban.definitions import GitRequire


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
def test_handle_requires_pypkg(fake_pip_install):
    modules = ["package1", "package2"]
    from moban.mobanfile import handle_requires

    handle_requires(modules)
    fake_pip_install.assert_called_with(modules)


@patch("moban.mobanfile.pip_install")
def test_handle_requires_pypkg_with_alternative_syntax(fake_pip_install):
    modules = [{"type": "pypi", "name": "pypi-mobans"}]
    from moban.mobanfile import handle_requires

    handle_requires(modules)
    fake_pip_install.assert_called_with(["pypi-mobans"])


@patch("moban.mobanfile.git_clone")
def test_handle_requires_repos(fake_git_clone):
    repos = ["https://github.com/my/repo", "https://gitlab.com/my/repo"]
    from moban.mobanfile import handle_requires

    expected = []
    for repo in repos:
        expected.append(GitRequire(git_url=repo, submodule=False))

    handle_requires(repos)
    fake_git_clone.assert_called_with(expected)


@patch("moban.mobanfile.git_clone")
def test_handle_requires_repos_with_alternative_syntax(fake_git_clone):
    repos = [{"type": "git", "url": "https://github.com/my/repo"}]
    from moban.mobanfile import handle_requires

    handle_requires(repos)
    fake_git_clone.assert_called_with(
        [GitRequire(git_url="https://github.com/my/repo")]
    )


@patch("moban.mobanfile.pip_install")
@patch("moban.mobanfile.git_clone")
def test_handle_requires_repos_with_submodule(
    fake_git_clone, fake_pip_install
):
    repos = [
        {"type": "git", "url": "https://github.com/my/repo", "submodule": True}
    ]
    from moban.mobanfile import handle_requires

    handle_requires(repos)
    fake_git_clone.assert_called_with(
        [GitRequire(git_url="https://github.com/my/repo", submodule=True)]
    )
    eq_(fake_pip_install.called, False)


def test_is_repo():
    repos = [
        "https://github.com/my/repo",
        "https://gitlab.com/my/repo",
        "https://bitbucket.com/my/repo",
        "https://unsupported.com/my/repo",
        "invalid/repo/url",
    ]
    from moban.mobanfile import is_repo

    actual = [is_repo(repo) for repo in repos]
    expected = [True, True, True, False, False]
    eq_(expected, actual)
