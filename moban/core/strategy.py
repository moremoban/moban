from collections import defaultdict

import moban.constants as constants
import moban.exceptions as exceptions


class Strategy(object):
    DATA_FIRST = 1
    TEMPLATE_FIRST = 2

    def __init__(self, array_of_param_tuple):
        self.data_file_index = defaultdict(list)
        self.template_file_index = defaultdict(list)
        self.tuples = array_of_param_tuple

    def process(self):
        for target in self.tuples:
            _append_to_array_item_to_dictionary_key(
                self.data_file_index,
                target.data_file,
                (target.template_file, target.output),
            )
            _append_to_array_item_to_dictionary_key(
                self.template_file_index,
                target.template_file,
                (target.data_file, target.output),
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
