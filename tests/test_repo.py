import os

from mock import patch
from moban.repo import (
    git_clone,
    get_repo_name,
    get_moban_home,
    make_sure_git_is_available,
)
from nose.tools import eq_, raises
from moban.exceptions import NoGitCommand
from moban.definitions import GitRequire


@patch("appdirs.user_cache_dir", return_value="root")
@patch("moban.utils.mkdir_p")
@patch("os.path.exists")
@patch("git.Repo", autospec=True)
class TestGitFunctions:
    def setUp(self):
        self.repo_name = "repoA"
        self.repo = "https://github.com/my/" + self.repo_name
        self.require = GitRequire(git_url=self.repo)
        self.require_with_submodule = GitRequire(
            git_url=self.repo, submodule=True
        )
        self.require_with_branch = GitRequire(
            git_url=self.repo, branch="ghpages"
        )
        self.require_with_reference = GitRequire(
            git_url=self.repo, reference="a-commit-reference"
        )
        self.expected_local_repo_path = os.path.join(
            "root", "repos", self.repo_name
        )

    def test_checkout_new(self, fake_repo, local_folder_exists, *_):
        local_folder_exists.return_value = False
        git_clone([self.require])
        fake_repo.clone_from.assert_called_with(
            self.repo,
            self.expected_local_repo_path,
            single_branch=True,
            depth=2,
        )
        repo = fake_repo.return_value
        eq_(repo.git.submodule.called, False)

    def test_checkout_new_with_submodules(
        self, fake_repo, local_folder_exists, *_
    ):
        local_folder_exists.return_value = False
        git_clone([self.require_with_submodule])
        fake_repo.clone_from.assert_called_with(
            self.repo,
            self.expected_local_repo_path,
            single_branch=True,
            depth=2,
        )
        repo = fake_repo.clone_from.return_value
        repo.git.submodule.assert_called_with("update", "--init")

    def test_git_update(self, fake_repo, local_folder_exists, *_):
        local_folder_exists.return_value = True
        git_clone([self.require])
        fake_repo.assert_called_with(self.expected_local_repo_path)
        repo = fake_repo.return_value
        repo.git.pull.assert_called()

    def test_git_update_with_submodules(
        self, fake_repo, local_folder_exists, *_
    ):
        local_folder_exists.return_value = True
        git_clone([self.require_with_submodule])
        fake_repo.assert_called_with(self.expected_local_repo_path)
        repo = fake_repo.return_value
        repo.git.submodule.assert_called_with("update")

    def test_checkout_new_with_branch(
        self, fake_repo, local_folder_exists, *_
    ):
        local_folder_exists.return_value = False
        git_clone([self.require_with_branch])
        fake_repo.clone_from.assert_called_with(
            self.repo,
            self.expected_local_repo_path,
            branch="ghpages",
            single_branch=True,
            depth=2,
        )
        repo = fake_repo.return_value
        eq_(repo.git.submodule.called, False)

    def test_update_existing_with_branch_parameter(
        self, fake_repo, local_folder_exists, *_
    ):
        local_folder_exists.return_value = True
        git_clone([self.require_with_branch])
        repo = fake_repo.return_value
        repo.git.checkout.assert_called_with("ghpages")

    def test_checkout_new_with_reference(
        self, fake_repo, local_folder_exists, *_
    ):
        local_folder_exists.return_value = False
        git_clone([self.require_with_reference])
        fake_repo.clone_from.assert_called_with(
            self.repo,
            self.expected_local_repo_path,
            reference="a-commit-reference",
            single_branch=True,
            depth=2,
        )
        repo = fake_repo.return_value
        eq_(repo.git.submodule.called, False)

    def test_update_existing_with_reference_parameter(
        self, fake_repo, local_folder_exists, *_
    ):
        local_folder_exists.return_value = True
        git_clone([self.require_with_reference])
        repo = fake_repo.return_value
        repo.git.checkout.assert_called_with("a-commit-reference")


def test_get_repo_name():
    repos = [
        "https://github.com/sphinx-doc/sphinx",
        "https://github.com/abc/repo",
        "https://github.com/abc/repo.git",
        "https://github.com/abc/repo/",
        "git@github.com:moremoban/moban.git",
    ]
    actual = [get_repo_name(repo) for repo in repos]
    expected = ["sphinx", "repo", "repo", "repo", "moban"]
    eq_(expected, actual)


@patch("moban.reporter.report_error_message")
def test_get_repo_name_can_handle_invalid_url(fake_reporter):
    invalid_repo = "invalid"
    try:
        get_repo_name(invalid_repo)
    except Exception:
        fake_reporter.assert_called_with(
            'An invalid git url: "invalid" in mobanfile'
        )


@patch("appdirs.user_cache_dir", return_value="root")
def test_get_moban_home(_):
    actual = get_moban_home()
    eq_(os.path.join("root", "repos"), actual)


@raises(NoGitCommand)
@patch("subprocess.check_output", side_effect=Exception)
def test_make_git_is_available(_):
    make_sure_git_is_available()
