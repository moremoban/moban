from mock import patch
from nose.tools import eq_

from moban.deprecated import GitRequire


@patch("moban.deprecated.pip_install")
def test_handle_requires_pypkg(fake_pip_install):
    modules = ["package1", "package2"]
    from moban.deprecated import handle_requires

    handle_requires(modules)
    fake_pip_install.assert_called_with(modules)


@patch("moban.deprecated.pip_install")
def test_handle_requires_pypkg_with_alternative_syntax(fake_pip_install):
    modules = [{"type": "pypi", "name": "pypi-mobans"}]
    from moban.mobanfile import handle_requires

    handle_requires(modules)
    fake_pip_install.assert_called_with(["pypi-mobans"])


@patch("moban.deprecated.git_clone")
def test_handle_requires_repos(fake_git_clone):
    repos = ["https://github.com/my/repo", "https://gitlab.com/my/repo"]
    from moban.mobanfile import handle_requires

    expected = []
    for repo in repos:
        expected.append(GitRequire(git_url=repo, submodule=False))

    handle_requires(repos)
    fake_git_clone.assert_called_with(expected)


@patch("moban.deprecated.git_clone")
def test_handle_requires_repos_with_alternative_syntax(fake_git_clone):
    repos = [{"type": "git", "url": "https://github.com/my/repo"}]
    from moban.mobanfile import handle_requires

    handle_requires(repos)
    fake_git_clone.assert_called_with(
        [GitRequire(git_url="https://github.com/my/repo")]
    )


@patch("moban.deprecated.pip_install")
@patch("moban.deprecated.git_clone")
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
    from moban.deprecated import is_repo

    actual = [is_repo(repo) for repo in repos]
    expected = [True, True, True, False, False]
    eq_(expected, actual)
