import logging

from moban import constants
from moban.externals import file_system

LOG = logging.getLogger(__name__)


def verify_the_existence_of_directories(dirs):
    if not isinstance(dirs, list):
        dirs = [dirs]

    dirs = [
        directory
        for directory in dirs
        if not (
            constants.DEFAULT_CONFIGURATION_DIRNAME in directory
            or constants.DEFAULT_TEMPLATE_DIRNAME in directory
        )
    ]
    if file_system.exists(constants.DEFAULT_CONFIGURATION_DIRNAME):
        dirs.append(constants.DEFAULT_CONFIGURATION_DIRNAME)

    if file_system.exists(constants.DEFAULT_TEMPLATE_DIRNAME):
        dirs.append(constants.DEFAULT_TEMPLATE_DIRNAME)
    return dirs
