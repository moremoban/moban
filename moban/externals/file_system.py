import os
import sys
import stat
import errno
import logging
from contextlib import contextmanager

import fs
import fs.path
from fs.multifs import MultiFS

from moban import exceptions

try:
    from urllib.parse import urlparse
except ImportError:
    from urlparse import urlparse


LOG = logging.getLogger(__name__)

path_join = fs.path.join
path_splitext = fs.path.splitext


def url_join(path, path2):
    result = urlparse(path)
    if result.scheme and path.endswith(result.scheme):
        return f"{path}!/{path2}"
    else:
        return f"{path}/{path2}"


def log_fs_failure(function_in_this_module):
    def wrapper(*args, **kwds):
        try:
            return function_in_this_module(*args, **kwds)
        except fs.errors.CreateFailed:
            message = "Failed to open %s" % args[0]
            LOG.debug(message)
            raise exceptions.FileNotFound(args[0])
        except fs.opener.errors.UnsupportedProtocol as e:
            LOG.exception(e)
            raise exceptions.UnsupportedPyFS2Protocol(e)

    return wrapper


@log_fs_failure
@contextmanager
def open_fs(path):
    if is_zip_alike_url(path):
        zip_file, folder = url_split(path)
        the_fs = fs.open_fs(zip_file)
    else:
        the_fs = fs.open_fs(path)
    try:
        yield the_fs
    finally:
        the_fs.close()


@log_fs_failure
@contextmanager
def open_file(path):
    if is_zip_alike_url(path):
        zip_file, folder = url_split(path)
        the_fs = fs.open_fs(zip_file)
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
def open_binary_file(path):
    if is_zip_alike_url(path):
        zip_file, folder = url_split(path)
        the_fs = fs.open_fs(zip_file)
        f = the_fs.openbin(folder)
    else:
        dir_name = fs.path.dirname(path)
        the_file_name = fs.path.basename(path)
        the_fs = fs.open_fs(dir_name)
        f = the_fs.openbin(the_file_name)
    try:
        yield f
    finally:
        f.close()
        the_fs.close()


@log_fs_failure
def read_unicode(path):
    with open_file(path) as file_handle:
        return file_handle.read()


@log_fs_failure
def read_bytes(path):
    with open_binary_file(path) as file_handle:
        return file_handle.read()


read_binary = read_bytes
read_text = read_unicode


@log_fs_failure
def write_bytes(filename, bytes_content):
    if "://" in filename:
        zip_file, folder = url_split(filename)
        with fs.open_fs(zip_file, create=True) as the_fs:
            the_fs.writebytes(folder, bytes_content)
    else:
        dir_name = fs.path.dirname(filename)
        the_file_name = fs.path.basename(filename)
        with fs.open_fs(dir_name) as the_fs:
            the_fs.writebytes(the_file_name, bytes_content)


@log_fs_failure
def is_dir(path):
    folder_or_file, path = _path_split(path)
    with fs.open_fs(folder_or_file) as the_fs:
        return the_fs.isdir(path)


@log_fs_failure
def is_file(path):
    folder_or_file, path = _path_split(path)
    with fs.open_fs(folder_or_file) as the_fs:
        return the_fs.isfile(path)


def exists(path):
    if is_zip_alike_url(path):
        zip_file, folder = url_split(path)
        try:
            with fs.open_fs(zip_file) as the_fs:
                if folder:
                    return the_fs.exists(folder)
                return True
        except fs.errors.CreateFailed:
            return False
        except fs.opener.errors.UnsupportedProtocol as e:
            LOG.exception(e)
            raise exceptions.UnsupportedPyFS2Protocol(e)
    dir_name = fs.path.dirname(path)
    the_file_name = fs.path.basename(path)

    try:
        with fs.open_fs(dir_name) as the_fs:
            return the_fs.exists(the_file_name)
    except fs.errors.CreateFailed:
        return False
    except fs.opener.errors.UnsupportedProtocol as e:
        LOG.exception(e)
        raise exceptions.UnsupportedPyFS2Protocol(e)


@log_fs_failure
def list_dir(path):
    folder_or_file, path = _path_split(path)
    with fs.open_fs(folder_or_file) as the_fs:
        for file_name in the_fs.listdir(path):
            yield file_name


@log_fs_failure
def abspath(path):
    folder_or_file, path = _path_split(path)
    with fs.open_fs(folder_or_file) as the_fs:
        return the_fs.getsyspath(path)


@log_fs_failure
def fs_url(path):
    folder_or_file, path = _path_split(path)
    with fs.open_fs(folder_or_file) as the_fs:
        return the_fs.geturl(path, purpose="fs")


@log_fs_failure
def system_path(path):
    folder_or_file, path = _path_split(path)
    with fs.open_fs(folder_or_file) as the_fs:
        return the_fs.getsyspath(path)


def to_unicode(path):
    return path


def is_zip_alike_url(url):
    specs = ["zip://", "tar://"]
    for prefix in specs:
        if url.startswith(prefix):
            return True
    else:
        return False


def file_permissions_copy(source, dest):
    source_permissions = file_permissions(source)
    dest_permissions = file_permissions(dest)

    if source_permissions != dest_permissions:
        os.chmod(dest, source_permissions)


def file_permissions(url):
    if not exists(url):
        raise exceptions.FileNotFound(url)
    if sys.platform == "win32":
        raise exceptions.NoPermissionsNeeded()
    elif is_zip_alike_url(url):
        raise exceptions.NoPermissionsNeeded()
    else:
        try:
            unix_path = system_path(url)
            return stat.S_IMODE(os.stat(unix_path).st_mode)
        except fs.errors.NoSysPath:
            raise exceptions.NoPermissionsNeeded()


def url_split(url):
    result = urlparse(url)

    if url.endswith(result.scheme):
        url_to_file = url
        path = None
    else:
        url_to_file, path = url.split("!/")

    return url_to_file, path


def _path_split(url_or_path):
    if is_zip_alike_url(url_or_path):
        return url_split(url_or_path)
    else:
        return fs.path.dirname(url_or_path), fs.path.basename(url_or_path)


def get_multi_fs(directories):
    filesystem = MultiFS()
    for directory in directories:
        filesystem.add_fs(directory, fs.open_fs(directory))
    return filesystem


def mkdir_p(path):
    try:
        os.makedirs(path)
    except OSError as exc:  # Python >2.5
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else:
            raise
