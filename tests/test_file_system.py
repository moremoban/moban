import os

from moban import file_system
from nose.tools import eq_

LOCAL_FOLDER = "tests/fixtures"
LOCAL_FILE = LOCAL_FOLDER + "/a.jj2"
ZIP_FILE = "zip://tests/fixtures/file_system/template-sources.zip"
TAR_FILE = "tar://tests/fixtures/file_system/template-sources.tar"

FILE = "file-in-template-sources-folder.txt"

ZIP_URL = ZIP_FILE + "/" + FILE
TAR_URL = TAR_FILE + "/" + FILE

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
    ["/tmp/test.binary", b"abc"],
    ["zip:///tmp/test.zip/test.binary", b"abc"],
    ["tar:///tmp/test.tar/test.binary", b"abc"],
]


def test_write_bytes():
    for url, content in TEST_WRITE_BYTES_SPEC:
        file_system.write_bytes(url, content)

    for url, expected in TEST_WRITE_BYTES_SPEC:
        content = file_system.read_bytes(url)
        eq_(content, expected)

    for file_name in ["/tmp/test.binary", "/tmp/test.zip", "/tmp/test.tar"]:
        os.unlink(file_name)


TEST_DIR_SPEC = [
    [LOCAL_FOLDER, True],
    [ZIP_FILE + "/dir-for-copying", True],
    [TAR_FILE + "/dir-for-copying", True],
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
    [ZIP_FILE + "/dir-for-copying", True],
    [TAR_FILE + "/dir-for-copying", True],
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
