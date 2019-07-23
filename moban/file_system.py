import sys

import fs
import fs.path

PY2 = sys.version_info[0] == 2


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


def abspath(path):
    path = to_unicode(path)
    dir_name = fs.path.dirname(path)
    the_file_name = fs.path.basename(path)
    with fs.open_fs(dir_name) as the_fs:
        return the_fs.getsyspath(the_file_name)


def to_unicode(path):
    if PY2:
        if isinstance(path, unicode) is False:
            return unicode(path)
    return path
