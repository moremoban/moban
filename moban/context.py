import os
import yaml


LABEL_OVERRIDES = 'overrides'
ERROR_DATA_FILE_NOT_FOUND = "Both %s and %s does not exist"
ERROR_DATA_FILE_ABSENT = "File %s does not exist"


class Context(object):
    def __init__(self, context_dirs):
        self.context_dirs = context_dirs

    def get_data(self, file_name):
        return open_yaml(self.context_dirs, file_name)


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


def open_yaml(base_dir, file_name):
    """
    chained yaml loader
    """
    the_file = file_name
    if not os.path.exists(the_file):
        if base_dir:
            the_file = os.path.join(base_dir, file_name)
            if not os.path.exists(the_file):
                raise IOError(
                    ERROR_DATA_FILE_NOT_FOUND % (file_name,
                                                 the_file))
        else:
            raise IOError(ERROR_DATA_FILE_ABSENT % the_file)
    with open(the_file, 'r') as data_yaml:
        data = yaml.load(data_yaml)
        if data is not None:
            parent_data = None
            if LABEL_OVERRIDES in data:
                parent_data = open_yaml(
                    base_dir,
                    data.pop(LABEL_OVERRIDES))
            if parent_data:
                return merge(data, parent_data)
            else:
                return data
        else:
            return None
