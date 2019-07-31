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


@log_fs_failure
@contextmanager
def open_file(path):
    path = to_unicode(path)
    if "zip://" in path:
        zip_file, folder = path.split(".zip/")
        the_fs = fs.open_fs(zip_file + ".zip")
        f = the_fs.open(folder)
    elif "tar://" in path:
        tar_file, folder = path.split(".tar/")
        the_fs = fs.open_fs(tar_file + ".tar")
        f = the_fs.open(folder)
    else:
        dir_name = fs.path.dirname(path)
        the_file_name = fs.path.basename(path)
        the_fs = fs.open_fs(dir_name)
        f = the_fs.open(the_file_name)
    try:
        yield f
    finally:
        f.close()
        the_fs.close()


@log_fs_failure
@contextmanager
def open_fs(path):
    path = to_unicode(path)
    if "zip://" in path:
        zip_file, folder = path.split(".zip")
        the_fs = fs.open_fs(zip_file + ".zip")
    elif "tar://" in path:
        tar_file, folder = path.split(".tar")
        the_fs = fs.open_fs(tar_file + ".tar")
    else:
        the_fs = fs.open_fs(path)
    try:
        yield the_fs
    finally:
        the_fs.close()


@log_fs_failure
def read_unicode(path):
    path = to_unicode(path)
    if "zip://" in path:
        zip_file, folder = path.split(".zip/")
        with fs.open_fs(zip_file + ".zip") as the_fs:
            with the_fs.open(folder) as file_handle:
                return file_handle.read()
    elif "tar://" in path:
        tar_file, folder = path.split(".tar/")
        with fs.open_fs(tar_file + ".tar") as the_fs:
            with the_fs.open(folder) as file_handle:
                return file_handle.read()
    else:
        dir_name = fs.path.dirname(path)
        the_file_name = fs.path.basename(path)

        with fs.open_fs(dir_name) as fs_system:
            with fs_system.open(the_file_name) as file_handle:
                return file_handle.read()


@log_fs_failure
def read_bytes(path):
    path = to_unicode(path)
    if "zip://" in path:
        zip_file, folder = path.split(".zip/")
        with fs.open_fs(zip_file + ".zip") as the_fs:
            return the_fs.readbytes(folder)
    elif "tar://" in path:
        tar_file, folder = path.split(".tar/")
        with fs.open_fs(tar_file + ".tar") as the_fs:
            return the_fs.readbytes(folder)
    else:
        dir_name = fs.path.dirname(path)
        the_file_name = fs.path.basename(path)
        with fs.open_fs(dir_name) as fs_system:
            return fs_system.readbytes(the_file_name)


read_binary = read_bytes


@log_fs_failure
def write_bytes(filename, bytes_content):
    if "zip://" in filename:
        zip_file, folder = filename.split(".zip/")
        with fs.open_fs(zip_file + ".zip", create=True) as the_fs:
            the_fs.writebytes(folder, bytes_content)

    elif "tar://" in filename:
        tar_file, folder = filename.split(".tar/")
        with fs.open_fs(tar_file + ".tar", create=True) as the_fs:
            the_fs.writebytes(folder, bytes_content)
    else:
        filename = to_unicode(filename)
        dir_name = fs.path.dirname(filename)
        the_file_name = fs.path.basename(filename)
        with fs.open_fs(dir_name) as the_fs:
            the_fs.writebytes(the_file_name, bytes_content)


@log_fs_failure
def is_dir(path):
    if "zip://" in path:
        zip_file, folder = path.split(".zip/")
        with fs.open_fs(zip_file + ".zip") as the_fs:
            return the_fs.isdir(to_unicode(folder))

    if "tar://" in path:
        zip_file, folder = path.split(".tar/")
        with fs.open_fs(zip_file + ".tar") as the_fs:
            return the_fs.isdir(to_unicode(folder))

    path = to_unicode(path)
    dir_name = fs.path.dirname(path)
    the_file_name = fs.path.basename(path)
    with fs.open_fs(dir_name) as the_fs:
        return the_fs.isdir(the_file_name)


@log_fs_failure
def is_file(path):
    path = to_unicode(path)
    dir_name = fs.path.dirname(path)
    the_file_name = fs.path.basename(path)
    with fs.open_fs(dir_name) as the_fs:
        return the_fs.isfile(the_file_name)


@log_fs_failure
def exists(path):
    path = to_unicode(path)

    if "zip://" in path:
        if path.endswith(".zip"):
            zip_file, folder = path, "/"
            try:
                with fs.open_fs(zip_file) as the_fs:
                    return True
            except fs.errors.CreateFailed:
                return False
        else:
            zip_file, folder = path.split(".zip/")
            try:
                with fs.open_fs(zip_file + ".zip") as the_fs:
                    return the_fs.exists(folder)
            except fs.errors.CreateFailed:
                return False

    if "tar://" in path:
        if path.endswith(".tar"):
            zip_file, folder = path, "/"
            try:
                with fs.open_fs(zip_file) as the_fs:
                    return True
            except fs.errors.CreateFailed:
                return False
        else:
            zip_file, folder = path.split(".tar/")
            try:
                with fs.open_fs(zip_file + ".tar") as the_fs:
                    return the_fs.exists(folder)
            except fs.errors.CreateFailed:
                return False

    dir_name = fs.path.dirname(path)
    the_file_name = fs.path.basename(path)

    try:
        with fs.open_fs(dir_name) as the_fs:
            return the_fs.exists(the_file_name)
    except fs.errors.CreateFailed:
        return False


@log_fs_failure
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


@log_fs_failure
def fs_url(path):
    path = to_unicode(path)
    dir_name = fs.path.dirname(path)
    the_file_name = fs.path.basename(path)

    with fs.open_fs(dir_name) as the_fs:
        return the_fs.geturl(the_file_name)


def to_unicode(path):
    if PY2 and path.__class__.__name__ != "unicode":
        return u"".__class__(path)
    return path
