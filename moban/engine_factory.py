import os
from collections import defaultdict

import moban.utils as utils
import moban.constants as constants
import moban.exceptions as exceptions
from lml.plugin import PluginManager


class EngineFactory(PluginManager):
    def __init__(self):
        super(EngineFactory, self).__init__(
            constants.TEMPLATE_ENGINE_EXTENSION
        )

    def get_engine(self, template_type):
        return self.load_me_now(template_type)

    def all_types(self):
        return list(self.registry.keys())

    def raise_exception(self, key):
        raise exceptions.NoThirdPartyEngine(key)


class Context(object):
    def __init__(self, context_dirs):
        verify_the_existence_of_directories(context_dirs)
        self.context_dirs = context_dirs
        self.__cached_environ_variables = dict(
            (key, os.environ[key]) for key in os.environ
        )

    def get_data(self, file_name):
        file_extension = os.path.splitext(file_name)[1]
        if file_extension == ".json":
            data = utils.open_json(self.context_dirs, file_name)
        elif file_extension in [".yml", ".yaml"]:
            data = utils.open_yaml(self.context_dirs, file_name)
            utils.merge(data, self.__cached_environ_variables)
        else:
            raise exceptions.IncorrectDataInput
        return data


class Strategy(object):
    DATA_FIRST = 1
    TEMPLATE_FIRST = 2

    def __init__(self, array_of_param_tuple):
        self.data_file_index = defaultdict(list)
        self.template_file_index = defaultdict(list)
        self.tuples = array_of_param_tuple

    def process(self):
        for (template_file, data_file, output_file) in self.tuples:
            _append_to_array_item_to_dictionary_key(
                self.data_file_index, data_file, (template_file, output_file)
            )
            _append_to_array_item_to_dictionary_key(
                self.template_file_index,
                template_file,
                (data_file, output_file),
            )

    def what_to_do(self):
        choice = Strategy.DATA_FIRST
        if self.data_file_index == {}:
            choice = Strategy.TEMPLATE_FIRST
        elif self.template_file_index != {}:
            data_files = len(self.data_file_index)
            template_files = len(self.template_file_index)
            if data_files > template_files:
                choice = Strategy.TEMPLATE_FIRST
        return choice


def _append_to_array_item_to_dictionary_key(adict, key, array_item):
    if array_item in adict[key]:
        raise exceptions.MobanfileGrammarException(
            constants.MESSAGE_SYNTAX_ERROR % (array_item, key)
        )
    else:
        adict[key].append(array_item)


def verify_the_existence_of_directories(dirs):
    if not isinstance(dirs, list):
        dirs = [dirs]

    for directory in dirs:
        if os.path.exists(directory):
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
                constants.MESSAGE_DIR_NOT_EXIST % os.path.abspath(directory)
            )
