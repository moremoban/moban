from nose.tools import eq_

from moban.definitions import GitRequire


def test_clone_params():
    require = GitRequire(git_url="http://github.com/some/repo")
    actual = require.clone_params()
    expected = {"single_branch": True}
    eq_(expected, actual)


def test_branch_params():
    require = GitRequire(
        git_url="http://github.com/some/repo", branch="ghpages"
    )
    actual = require.clone_params()
    expected = {"single_branch": True, "branch": "ghpages"}
    eq_(expected, actual)
