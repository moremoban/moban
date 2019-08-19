import os

from moban import utils, reporter, exceptions
from moban.data_loaders.manager import load_data


class Context(object):
    def __init__(self, context_dirs):
        utils.verify_the_existence_of_directories(context_dirs)
        self.context_dirs = context_dirs
        self.__cached_environ_variables = dict(
            (key, os.environ[key]) for key in os.environ
        )

    def get_data(self, file_name):
        try:
            data = load_data(self.context_dirs, file_name)
            utils.merge(data, self.__cached_environ_variables)
            return data
        except (IOError, exceptions.IncorrectDataInput) as exception:
            # If data file doesn't exist:
            # 1. Alert the user of their (potential) mistake
            # 2. Attempt to use environment vars as data
            reporter.report_warning_message(str(exception))
            reporter.report_using_env_vars()
            return self.__cached_environ_variables
