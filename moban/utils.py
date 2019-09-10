import os
import errno
import logging

from moban import constants, exceptions, file_system

LOG = logging.getLogger(__name__)


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
