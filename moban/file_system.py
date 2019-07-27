import sys
import logging
from contextlib import contextmanager

import fs
import fs.path

PY2 = sys.version_info[0] == 2
LOG = logging.getLogger(__name__)

path_join = fs.path.join
path_splitext = fs.path.splitext


def log_fs_failure(function_in_this_module):
    def wrapper(*args, **kwds):
        try:
            return function_in_this_module(*args, **kwds)
        except fs.errors.CreateFailed:
            from moban import reporter

            message = "Failed to open %s" % args[0]
            LOG.debug(message)
            reporter.report_error_message(message)
            raise

    return wrapper


@contextmanager
def open_fs(path):
    path = to_unicode(path)
    dir_name = fs.path.dirname(path)
    the_file_name = fs.path.basename(path)
    the_fs = fs.open_fs(dir_name)
    f = the_fs.open(the_file_name)
    try:
        yield f
    finally:
        f.close()
        the_fs.close()


def read_unicode(path):
    path = to_unicode(path)
    dir_name = fs.path.dirname(path)
    the_file_name = fs.path.basename(path)
    with fs.open_fs(dir_name) as fs_system:
        with fs_system.open(the_file_name) as file_handle:
            return file_handle.read()


def write_bytes(filename, bytes_content):
    filename = to_unicode(filename)
    dir_name = fs.path.dirname(filename)
    the_file_name = fs.path.basename(filename)
    with fs.open_fs(dir_name) as the_fs:
        the_fs.writebytes(the_file_name, bytes_content)


def is_dir(path):
    path = to_unicode(path)
    dir_name = fs.path.dirname(path)
    the_file_name = fs.path.basename(path)
    with fs.open_fs(dir_name) as the_fs:
        return the_fs.isdir(the_file_name)


def is_file(path):
    path = to_unicode(path)
    dir_name = fs.path.dirname(path)
    the_file_name = fs.path.basename(path)
    with fs.open_fs(dir_name) as the_fs:
        return the_fs.isfile(the_file_name)


def exists(path):
    path = to_unicode(path)
    dir_name = fs.path.dirname(path)
    the_file_name = fs.path.basename(path)
    try:
        with fs.open_fs(dir_name) as the_fs:
            return the_fs.exists(the_file_name)
    except fs.errors.CreateFailed:
        return False


def list_dir(path):
    path = to_unicode(path)
    dir_name = fs.path.dirname(path)
    the_file_name = fs.path.basename(path)
    with fs.open_fs(dir_name) as fs_system:
        for file_name in fs_system.listdir(the_file_name):
            yield file_name


@log_fs_failure
def abspath(path):
    path = to_unicode(path)
    dir_name = fs.path.dirname(path)
    the_file_name = fs.path.basename(path)

    with fs.open_fs(dir_name) as the_fs:
        return the_fs.getsyspath(the_file_name)


def to_unicode(path):
    if PY2 and path.__class__.__name__ != "unicode":
        return u"".__class__(path)
    return path
