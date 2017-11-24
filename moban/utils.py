import os
import sys
import stat

import yaml

import moban.constants as constants
import moban.exceptions as exceptions


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
    the_yaml_file = search_file(base_dir, file_name)
    with open(the_yaml_file, 'r') as data_yaml:
        data = yaml.load(data_yaml)
        if data is not None:
            parent_data = None
            if base_dir and constants.LABEL_OVERRIDES in data:
                parent_data = open_yaml(
                    base_dir,
                    data.pop(constants.LABEL_OVERRIDES))
            if parent_data:
                return merge(data, parent_data)
            else:
                return data
        else:
            return None


def search_file(base_dir, file_name):
    the_file = file_name
    if not os.path.exists(the_file):
        if base_dir:
            the_file = os.path.join(base_dir, file_name)
            if not os.path.exists(the_file):
                raise IOError(
                    constants.ERROR_DATA_FILE_NOT_FOUND % (
                        file_name, the_file))
        else:
            raise IOError(constants.ERROR_DATA_FILE_ABSENT % the_file)
    return the_file


def parse_targets(options, targets):
    common_data_file = options[constants.LABEL_CONFIG]
    for target in targets:
        if constants.LABEL_OUTPUT in target:
            template_file = target.get(
                constants.LABEL_TEMPLATE,
                options.get(constants.LABEL_TEMPLATE, None))
            data_file = target.get(constants.LABEL_CONFIG,
                                   common_data_file)
            output = target[constants.LABEL_OUTPUT]
            yield((template_file, data_file, output))
        else:
            for output, template_file in target.items():
                yield((template_file, common_data_file, output))


def load_external_engine(template_type):
    module_name = "%s_%s" % (constants.PROGRAM_NAME, template_type)
    try:
        __import__(module_name)
    except ImportError:
        raise
    module = sys.modules[module_name]
    return module


def file_permissions_copy(source, dest):
    source_permissions = file_permissions(source)
    dest_permissions = file_permissions(dest)
    if source_permissions != dest_permissions:
        os.chmod(dest, source_permissions)


def file_permissions(afile):
    if not os.path.exists(afile):
        raise exceptions.FileNotFound(afile)
    return stat.S_IMODE(os.lstat(afile).st_mode)
