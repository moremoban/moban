import os
import sys
import stat
from shutil import rmtree

from mock import patch
from nose import SkipTest
from nose.tools import eq_, raises
from moban.utils import (
    mkdir_p,
    write_file_out,
    file_permissions,
    get_template_path,
    file_permissions_copy,
)
from moban.exceptions import FileNotFound


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
    content = b"""
    helloworld




    """
    test_file = "testout"
    write_file_out(test_file, content)
    with open(test_file, "r") as f:
        content = f.read()
        eq_(content, "\n    helloworld\n\n\n\n\n    ")


def test_mkdir_p():
    test_path = "a/b/c/d"
    mkdir_p(test_path)
    assert os.path.exists(test_path)
    rmtree(test_path)


@raises(FileNotFound)
def test_get_template_path_with_error():
    temp_dirs = [
        os.path.join("tests", "fixtures", "template-tests"),
        os.path.join("tests", "abc"),
    ]
    template = "I-do-not-exist.jj2"
    get_template_path(temp_dirs, template)


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
