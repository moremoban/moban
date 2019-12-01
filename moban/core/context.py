import os
import copy
import logging

from moban import constants, exceptions
from moban.core import utils
from moban.program_options import OPTIONS
from moban.core.data_loader import merge, load_data

LOG = logging.getLogger(__name__)
MESSAGE_USING_ENV_VARS = "Attempting to use environment vars as data..."


class Context(object):
    def __init__(self, context_dirs):
        utils.verify_the_existence_of_directories(context_dirs)
        self.context_dirs = context_dirs
        self.__cached_environ_variables = dict(
            (key, os.environ[key]) for key in os.environ
        )

    def get_data(self, file_name):
        custom_data = copy.deepcopy(OPTIONS[constants.CLI_DICT])
        try:
            data = load_data(self.context_dirs, file_name)
            merge(custom_data, data)
            merge(custom_data, self.__cached_environ_variables)
            return custom_data
        except (IOError, exceptions.IncorrectDataInput) as exception:
            # If data file doesn't exist:
            # 1. Alert the user of their (potential) mistake
            # 2. Attempt to use environment vars as data
            LOG.warn(str(exception))
            LOG.info(MESSAGE_USING_ENV_VARS)
            merge(custom_data, self.__cached_environ_variables)
            return custom_data
