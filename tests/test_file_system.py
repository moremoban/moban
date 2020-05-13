import os
import sys
import stat
from shutil import rmtree

from mock import patch
from nose import SkipTest
from nose.tools import eq_, raises

from moban.externals import file_system
from moban.exceptions import FileNotFound, UnsupportedPyFS2Protocol

LOCAL_FOLDER = "tests/fixtures"
LOCAL_FILE = LOCAL_FOLDER + "/a.jj2"
ZIP_FILE = "zip://tests/fixtures/file_system/template-sources.zip"
TAR_FILE = "tar://tests/fixtures/file_system/template-sources.tar"

FILE = "file-in-template-sources-folder.txt"

ZIP_URL = ZIP_FILE + "!/" + FILE
TAR_URL = TAR_FILE + "!/" + FILE

TEST_SPECS = [LOCAL_FILE, ZIP_URL, TAR_URL]


TEST_FS_SPECS = [LOCAL_FOLDER, ZIP_FILE, TAR_FILE]


def test_open_file():
    for url in TEST_SPECS:
        with file_system.open_file(url):
            pass


def test_open_fs():
    for url in TEST_FS_SPECS:
        with file_system.open_fs(url):
            pass


TEST_FILE_CONTENT_SPECS = [
    [LOCAL_FILE, "{{key}} {{pass}}"],
    [ZIP_URL, "test file\n"],
    [TAR_URL, "test file\n"],
]


def test_read_unicode():
    for url, expected in TEST_FILE_CONTENT_SPECS:
        content = file_system.read_unicode(url)
        eq_(content, expected)


TEST_FILE_CONTENT_SPECS_BINARY = [
    [LOCAL_FILE, b"{{key}} {{pass}}"],
    [ZIP_URL, b"test file\n"],
    [TAR_URL, b"test file\n"],
]


def test_read_binary():
    for url, expected in TEST_FILE_CONTENT_SPECS_BINARY:
        content = file_system.read_binary(url)
        eq_(content, expected)


TEST_WRITE_BYTES_SPEC = [
    ["test.binary", b"abc"],
    ["zip://test.zip!/test.binary", b"abc"],
    ["tar://test.tar!/test.binary", b"abc"],
]


def test_write_bytes():
    for url, content in TEST_WRITE_BYTES_SPEC:
        file_system.write_bytes(url, content)

    for url, expected in TEST_WRITE_BYTES_SPEC:
        content = file_system.read_bytes(url)
        eq_(content, expected)

    for file_name in ["test.binary", "test.zip", "test.tar"]:
        os.unlink(file_name)


TEST_DIR_SPEC = [
    [LOCAL_FOLDER, True],
    [ZIP_FILE + "!/dir-for-copying", True],
    [TAR_FILE + "!/dir-for-copying", True],
    [ZIP_URL, False],
    [TAR_URL, False],
    [LOCAL_FILE, False],
]


def test_is_dir():
    for url, expected in TEST_DIR_SPEC:
        status = file_system.is_dir(url)
        eq_(status, expected)


def test_is_file():
    for url, is_dir in TEST_DIR_SPEC:
        status = file_system.is_file(url)
        expected = not is_dir
        eq_(status, expected)


TEST_URL_EXITENCE_SPEC = [
    [LOCAL_FOLDER, True],
    [ZIP_FILE + "!/dir-for-copying", True],
    [TAR_FILE + "!/dir-for-copying", True],
    [ZIP_URL, True],
    [TAR_URL, True],
    [LOCAL_FILE, True],
    # ['zip://abc.zip', False],
    # ['tar://abc.tar', False], bug with fs.zipfs. raise it later
    ["abcx", False],
]


def test_exists():
    for url, expected in TEST_URL_EXITENCE_SPEC:
        status = file_system.exists(url)
        eq_(status, expected)


@raises(UnsupportedPyFS2Protocol)
def test_exists_raise_exception():
    file_system.exists("git2://protocol/abc")


@raises(UnsupportedPyFS2Protocol)
def test_is_file_raise_exception():
    file_system.is_file("git2://protocol/abc")


TEST_LIST_DIR_SPEC = [
    [
        LOCAL_FOLDER + "/file_system",
        ["template-sources.zip", "template-sources.tar"],
    ],
    [
        ZIP_FILE + "!/dir-for-copying",
        ["afile.txt", "sub_directory_is_not_copied"],
    ],
    [
        TAR_FILE + "!/dir-for-copying",
        ["afile.txt", "sub_directory_is_not_copied"],
    ],
]


def test_list_dir():
    for url, expected in TEST_LIST_DIR_SPEC:
        file_list = sorted(list(file_system.list_dir(url)))
        eq_(file_list, sorted(expected))


TEST_FILE_PATH = [
    [
        LOCAL_FOLDER + "/file_system",
        os.path.normpath(
            os.path.join(os.getcwd(), "tests/fixtures/file_system")
        ),
    ]
]


def test_abspath():
    for path, expected in TEST_FILE_PATH:
        url = file_system.abspath(path)
        eq_(url, expected)


TEST_FILE_URL = [
    [
        LOCAL_FOLDER + "/file_system",
        "osfs://"
        + os.path.normpath(
            os.path.join(os.getcwd(), "tests/fixtures/file_system")
        ),
    ]
]


def test_fs_url():
    for path, expected in TEST_FILE_URL:
        url = file_system.fs_url(path)
        eq_(url, expected.replace("\\", "/"))


URL_JOIN_TEST_FIXTURES = [
    ["parent", "child", "parent/child"],
    ["zip://test.zip", "file", "zip://test.zip!/file"],
    ["/root", "path", "/root/path"],
]


def test_url_join():
    for parent, child, expected_path in URL_JOIN_TEST_FIXTURES:
        actual = file_system.url_join(parent, child)
        eq_(actual, expected_path)


def create_file(test_file, permission):
    with open(test_file, "w") as f:
        f.write("test")

    os.chmod(test_file, permission)


def test_file_permission_copy():
    if sys.platform == "win32":
        raise SkipTest("No actual chmod on windows")
    test_source = "test_file_permission_copy1"
    test_dest = "test_file_permission_copy2"
    create_file(test_source, 0o755)
    create_file(test_dest, 0o646)
    file_system.file_permissions_copy(test_source, test_dest)
    eq_(
        stat.S_IMODE(os.lstat(test_source).st_mode),
        stat.S_IMODE(os.lstat(test_dest).st_mode),
    )
    os.unlink(test_source)
    os.unlink(test_dest)


def file_permissions_disabled_on_windows():
    if sys.platform == "win32":
        permissions = file_system.file_permissions("abc")
        eq_("no-permission-support", permissions)
    else:
        raise SkipTest("No test required")


@raises(FileNotFound)
def test_file_permissions_file_not_found():
    file_system.file_permissions("I does not exist")


def test_file_permission_copy_symlink():
    if sys.platform == "win32":
        raise SkipTest("No symlink on windows")
    test_source = "test_file_permission_copy1"
    test_dest = "test_file_permission_copy2"
    test_symlink = "test_file_permission_symlink"
    create_file(test_source, 0o046)
    os.symlink(test_source, test_symlink)
    create_file(test_dest, 0o646)
    file_system.file_permissions_copy(test_source, test_dest)
    eq_(
        stat.S_IMODE(os.lstat(test_source).st_mode),
        stat.S_IMODE(os.lstat(test_dest).st_mode),
    )
    os.unlink(test_source)
    os.unlink(test_dest)
    os.unlink(test_symlink)


def test_mkdir_p():
    test_path = "a/b/c/d"
    file_system.mkdir_p(test_path)
    assert os.path.exists(test_path)
    rmtree(test_path)


@patch("subprocess.check_call")
def test_pip_install(fake_check_all):
    import sys
    from moban.deprecated import pip_install

    pip_install(["package1", "package2"])
    fake_check_all.assert_called_with(
        [sys.executable, "-m", "pip", "install", "package1 package2"],
        stderr=-3,
        stdout=-3,
    )
