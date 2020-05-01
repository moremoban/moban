import logging

from moban import constants

LOG = logging.getLogger(__name__)


def verify_the_existence_of_directories(dirs):
    if not isinstance(dirs, list):
        dirs = [dirs]

    return [
        directory
        for directory in dirs
        if not (
            constants.DEFAULT_CONFIGURATION_DIRNAME in directory
            or constants.DEFAULT_TEMPLATE_DIRNAME in directory
        )
    ]
