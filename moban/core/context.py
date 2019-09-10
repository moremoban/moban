import os
import copy

from moban import utils, reporter, constants, exceptions
from moban.program_options import OPTIONS
from moban.data_loaders.manager import merge, load_data


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
            reporter.report_warning_message(str(exception))
            reporter.report_using_env_vars()
            merge(custom_data, self.__cached_environ_variables)
            return custom_data
