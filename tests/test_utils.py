import os
import sys
import stat
from shutil import rmtree

from mock import patch
from nose import SkipTest
from nose.tools import eq_, raises

from moban.utils import (
    mkdir_p,
    git_clone,
    get_repo_name,
    get_moban_home,
    write_file_out,
    handle_template,
    file_permissions,
    get_template_path,
    file_permissions_copy,
    strip_off_trailing_new_lines,
)
from moban.exceptions import FileNotFound
from moban.definitions import GitRequire


def create_file(test_file, permission):
    with open(test_file, "w") as f:
        f.write("test")

    os.chmod(test_file, permission)


def test_file_permission_copy():
    if sys.platform == "win32":
        raise SkipTest("No actual chmod on windows")
    test_source = "test_file_permission_copy1"
    test_dest = "test_file_permission_copy2"
    create_file(test_source, 0o046)
    create_file(test_dest, 0o646)
    file_permissions_copy(test_source, test_dest)
    eq_(
        stat.S_IMODE(os.lstat(test_source).st_mode),
        stat.S_IMODE(os.lstat(test_dest).st_mode),
    )
    os.unlink(test_source)
    os.unlink(test_dest)


def file_permissions_disabled_on_windows():
    if sys.platform == "win32":
        permissions = file_permissions("abc")
        eq_("no-permission-support", permissions)
    else:
        raise SkipTest("No test required")


@raises(FileNotFound)
def test_file_permissions_file_not_found():
    file_permissions("I does not exist")


def test_file_permission_copy_symlink():
    if sys.platform == "win32":
        raise SkipTest("No symlink on windows")
    test_source = "test_file_permission_copy1"
    test_dest = "test_file_permission_copy2"
    test_symlink = "test_file_permission_symlink"
    create_file(test_source, 0o046)
    os.symlink(test_source, test_symlink)
    create_file(test_dest, 0o646)
    file_permissions_copy(test_source, test_dest)
    eq_(
        stat.S_IMODE(os.lstat(test_source).st_mode),
        stat.S_IMODE(os.lstat(test_dest).st_mode),
    )
    os.unlink(test_source)
    os.unlink(test_dest)
    os.unlink(test_symlink)


def test_write_file_out():
    content = """
    helloworld




    """
    test_file = "testout"
    write_file_out(test_file, content)
    with open(test_file, "r") as f:
        content = f.read()
        eq_(content, "\n    helloworld\n")


def test_strip_new_lines():
    content = "test\n\n\n\n\n"
    actual = strip_off_trailing_new_lines(content)
    eq_(actual, "test\n")


def test_mkdir_p():
    test_path = "a/b/c/d"
    mkdir_p(test_path)
    assert os.path.exists(test_path)
    rmtree(test_path)


def test_get_template_path():
    temp_dirs = [
        os.path.join("tests", "fixtures", "template-tests"),
        os.path.join("tests", "abc"),
        os.path.join("tests", "abc"),
    ]
    template = "a.jj2"
    template_path = get_template_path(temp_dirs, template)
    expected = os.path.join(
        os.getcwd(),
        os.path.join("tests", "fixtures", "template-tests", "a.jj2"),
    )
    eq_(template_path, expected)


@patch("subprocess.check_call")
def test_pip_install(fake_check_all):
    import sys
    from moban.utils import pip_install

    pip_install(["package1", "package2"])
    fake_check_all.assert_called_with(
        [sys.executable, "-m", "pip", "install", "package1 package2"]
    )


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
        self.expected_local_repo_path = os.path.join(
            "root", "repos", self.repo_name
        )

    def test_checkout_new(self, fake_repo, local_folder_exists, *_):
        local_folder_exists.return_value = False
        git_clone([self.require])
        fake_repo.clone_from.assert_called_with(
            self.repo, self.expected_local_repo_path, single_branch=True
        )
        repo = fake_repo.return_value
        eq_(repo.git.submodule.called, False)

    def test_checkout_new_with_submodules(
        self, fake_repo, local_folder_exists, *_
    ):
        local_folder_exists.return_value = False
        git_clone([self.require_with_submodule])
        fake_repo.clone_from.assert_called_with(
            self.repo, self.expected_local_repo_path, single_branch=True
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
        )
        repo = fake_repo.return_value
        eq_(repo.git.submodule.called, False)


def test_get_repo_name():
    repos = [
        "https://github.com/abc/repo",
        "https://github.com/abc/repo.git",
        "https://github.com/abc/repo/",
        "git@github.com:moremoban/moban.git",
    ]
    actual = [get_repo_name(repo) for repo in repos]
    expected = ["repo", "repo", "repo", "moban"]
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


class TestHandleTemplateFunction:
    def setUp(self):
        self.base_dir = [os.path.join("tests", "fixtures")]

    def test_copy_files(self):
        results = list(
            handle_template("copier-test01.csv", "/tmp/test", self.base_dir)
        )
        expected = [("copier-test01.csv", "/tmp/test", "csv")]
        eq_(expected, results)

    @patch("moban.reporter.report_error_message")
    def test_file_not_found(self, reporter):
        list(
            handle_template(
                "copier-test-not-found.csv", "/tmp/test", self.base_dir
            )
        )
        reporter.assert_called_with(
            "copier-test-not-found.csv cannot be found"
        )

    def test_listing_dir(self):
        test_dir = "/tmp/copy-a-directory"
        results = list(
            handle_template("copier-directory", test_dir, self.base_dir)
        )
        expected = [
            (
                "copier-directory/level1-file1",
                "/tmp/copy-a-directory/level1-file1",
                None,
            )
        ]
        eq_(expected, results)

    def test_listing_dir_recusively(self):
        test_dir = "/tmp/copy-a-directory"
        results = list(
            handle_template("copier-directory/**", test_dir, self.base_dir)
        )
        expected = [
            (
                "copier-directory/copier-sample-dir/file1",
                "/tmp/copy-a-directory/copier-sample-dir/file1",
                None,
            ),
            (
                "copier-directory/level1-file1",
                "/tmp/copy-a-directory/level1-file1",
                None,
            ),
        ]
        eq_(expected, results)

    @patch("moban.reporter.report_error_message")
    def test_listing_dir_recusively_with_error(self, reporter):
        test_dir = "/tmp/copy-a-directory"
        list(
            handle_template(
                "copier-directory-does-not-exist/**", test_dir, self.base_dir
            )
        )
        eq_(reporter.call_count, 1)
