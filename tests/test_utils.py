import os
import stat
from shutil import rmtree

from mock import Mock, patch
from nose.tools import eq_, raises
from moban.utils import (
    mkdir_p,
    get_repo_name,
    write_file_out,
    file_permissions,
    get_template_path,
    expand_directories,
    file_permissions_copy,
    strip_off_trailing_new_lines,
)
from moban.exceptions import FileNotFound


def create_file(test_file, permission):
    with open(test_file, "w") as f:
        f.write("test")

    os.chmod(test_file, permission)


def test_file_permission_copy():
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


@raises(FileNotFound)
def test_file_permissions_file_not_found():
    file_permissions("I does not exist")


def test_file_permission_copy_symlink():
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


def test_expand_dir():
    file_list = [("template-tests", "abc", "abc")]
    template_dirs = [os.path.join("tests", "fixtures")]
    results = list(expand_directories(file_list, template_dirs))
    expected = [("template-tests/a.jj2", "abc", "abc/a")]
    eq_(results, expected)


def test_get_template_path():
    temp_dirs = ["tests/fixtures/template-tests", "tests/abc", "tests/abc"]
    template = Mock()
    template.filename = "a.jj2"
    template_path = get_template_path(temp_dirs, template)
    expected = os.path.join(os.getcwd(), "tests/fixtures/template-tests/a.jj2")
    eq_(template_path, expected)


@patch("subprocess.check_call")
def test_pip_install(fake_check_all):
    import sys
    from moban.utils import pip_install

    pip_install(["package1", "package2"])
    fake_check_all.assert_called_with(
        [sys.executable, "-m", "pip", "install", "package1 package2"]
    )


@patch("subprocess.check_call")
def test_git_clone(fake_check_all):
    from moban.utils import git_clone

    git_clone(["https://github.com/my/repo", "https://gitlab.com/my/repo"])
    fake_check_all.assert_called_with(
        ["git", "clone", "https://gitlab.com/my/repo", "repo"]
    )


@patch("os.chdir")
@patch("subprocess.check_call")
def test_git_clone_with_submodules(fake_check_all, _):
    from moban.utils import git_clone

    git_clone(
        ["https://github.com/my/repo", "https://gitlab.com/my/repo"],
        submodule=True,
    )
    fake_check_all.assert_called_with(["git", "submodule", "update"])


@patch("os.path.exists", return_value=True)
@patch("os.chdir")
@patch("subprocess.check_call")
def test_git_clone_with_existing_repo(fake_check_all, _, __):
    from moban.utils import git_clone

    git_clone(
        ["https://github.com/my/repo", "https://gitlab.com/my/repo"],
        submodule=True,
    )
    fake_check_all.assert_called_with(["git", "submodule", "update"])


def test_get_repo_name():
    repos = ["https://github.com/abc/repo", "https://github.com/abc/repo/"]
    actual = [get_repo_name(repo) for repo in repos]
    expected = ["repo", "repo"]
    eq_(expected, actual)
