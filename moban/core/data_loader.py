import logging
from collections import OrderedDict

from lml.plugin import PluginManager
from ruamel.yaml.comments import CommentedSeq

from moban import constants
from moban.externals import file_system

LOG = logging.getLogger()


class AnyDataLoader(PluginManager):
    def __init__(self):
        super(AnyDataLoader, self).__init__(constants.DATA_LOADER_EXTENSION)

    def get_data(self, file_name):
        file_extension = file_system.path_splitext(file_name)[1]
        file_type = file_extension
        if file_extension.startswith("."):
            file_type = file_type[1:]

        try:
            loader_function = self.load_me_now(file_type)
        except Exception:
            loader_function = self.load_me_now(constants.DEFAULT_DATA_TYPE)
        return loader_function(file_name)


LOADER = AnyDataLoader()


def load_data(base_dir, file_name):
    abs_file_path = search_file(base_dir, file_name)
    data = LOADER.get_data(abs_file_path)
    if data is not None:
        parent_data = OrderedDict()
        if constants.LABEL_OVERRIDES in data:
            overrides = data.pop(constants.LABEL_OVERRIDES)
            if not isinstance(overrides, list):
                overrides = [overrides]
            for parent_file in overrides:
                file_name, key = parent_file, None
                results = match_fs_url(parent_file)
                if results:
                    file_name, key = results
                elif ":" in parent_file and "://" not in parent_file:
                    file_name, key = parent_file.split(":")
                try:
                    child_data = load_data(base_dir, file_name)
                except IOError:
                    LOG.warn(f"failed to load {file_name} in {base_dir}")
                    child_data = {}
                if data:
                    if key:
                        child_data = OrderedDict({key: child_data[key]})
                    parent_data = merge(parent_data, child_data)
        if parent_data:
            return merge(data, parent_data)
        else:
            return data
    else:
        return None


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
    else:
        both_list_alike = (
            isinstance(left, CommentedSeq) and isinstance(right, CommentedSeq)
        ) or (isinstance(left, list) and isinstance(right, list))
        if both_list_alike:
            left.extend(right)
    return left


def search_file(base_dir, file_name):
    the_file = file_name
    if not file_system.exists(the_file):
        if base_dir:
            file_under_base_dir = file_system.url_join(base_dir, the_file)
            if file_system.exists(file_under_base_dir):
                the_file = file_system.fs_url(file_under_base_dir)
            else:
                raise IOError(
                    constants.ERROR_DATA_FILE_NOT_FOUND % (file_name, the_file)
                )
        else:
            raise IOError(constants.ERROR_DATA_FILE_ABSENT % the_file)
    return the_file


def match_fs_url(file_name):
    import re

    results = re.match("(.*://.*):(.*)", file_name)
    if results:
        return (results.group(1), results.group(2))
