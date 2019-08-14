import os
import sys
import errno
import logging

from moban import constants, exceptions, file_system

LOG = logging.getLogger(__name__)
PY2 = sys.version_info[0] == 2


def merge(left, right):
    """
    deep merge dictionary on the left with the one
    on the right.

    Fill in left dictionary with right one where
    the value of the key from the right one in
    the left one is missing or None.
    """
    if isinstance(left, dict) and isinstance(right, dict):
        for key, value in right.items():
            if key not in left:
                left[key] = value
            elif left[key] is None:
                left[key] = value
            else:
                left[key] = merge(left[key], value)
    return left


def mkdir_p(path):
    try:
        os.makedirs(path)
    except OSError as exc:  # Python >2.5
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else:
            raise


def verify_the_existence_of_directories(dirs):
    LOG.debug("Verifying the existence: %s", dirs)
    if not isinstance(dirs, list):
        dirs = [dirs]

    results = []

    for directory in dirs:

        if file_system.exists(directory):
            results.append(directory)
            continue
        should_I_ignore = (
            constants.DEFAULT_CONFIGURATION_DIRNAME in directory
            or constants.DEFAULT_TEMPLATE_DIRNAME in directory
        )
        if should_I_ignore:
            # ignore
            pass
        else:
            raise exceptions.DirectoryNotFound(
                constants.MESSAGE_DIR_NOT_EXIST % directory
            )
    return results
