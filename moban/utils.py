import os
import re
import stat
import errno

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
    with open(the_yaml_file, "r") as data_yaml:
        data = yaml.load(data_yaml)
        if data is not None:
            parent_data = None
            if base_dir and constants.LABEL_OVERRIDES in data:
                parent_data = open_yaml(
                    base_dir, data.pop(constants.LABEL_OVERRIDES)
                )
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
                    constants.ERROR_DATA_FILE_NOT_FOUND % (file_name, the_file)
                )
        else:
            raise IOError(constants.ERROR_DATA_FILE_ABSENT % the_file)
    return the_file


def parse_targets(options, targets):
    common_data_file = options[constants.LABEL_CONFIG]
    for target in targets:
        if constants.LABEL_OUTPUT in target:
            template_file = target.get(
                constants.LABEL_TEMPLATE,
                options.get(constants.LABEL_TEMPLATE, None),
            )
            data_file = target.get(constants.LABEL_CONFIG, common_data_file)
            output = target[constants.LABEL_OUTPUT]
            yield ((template_file, data_file, output))
        else:
            for output, template_file in target.items():
                yield ((template_file, common_data_file, output))


def expand_directories(file_list, template_dirs):
    for template_file, data_file, output in file_list:
        true_template_file = template_file
        for a_template_dir in template_dirs:
            true_template_file = os.path.join(a_template_dir, template_file)
            if os.path.exists(true_template_file):
                break
        if os.path.isdir(true_template_file):
            for file_name in os.listdir(true_template_file):
                base_output_name, _ = os.path.splitext(file_name)
                yield (
                    (
                        os.path.join(template_file, file_name),
                        data_file,
                        os.path.join(output, base_output_name),
                    )
                )
        else:
            yield ((template_file, data_file, output))


def file_permissions_copy(source, dest):
    source_permissions = file_permissions(source)
    dest_permissions = file_permissions(dest)
    if source_permissions != dest_permissions:
        os.chmod(dest, source_permissions)


def file_permissions(afile):
    if not os.path.exists(afile):
        raise exceptions.FileNotFound(afile)
    return stat.S_IMODE(os.stat(afile).st_mode)


def strip_off_trailing_new_lines(content):
    return re.sub("(\n\s+)+$", "\n", content)


def write_file_out(filename, content, strip=True, encode=True):
    dest_folder = os.path.dirname(filename)
    if dest_folder:
        mkdir_p(dest_folder)
    with open(filename, "wb") as out:
        if strip:
            content = strip_off_trailing_new_lines(content)
        if encode:
            content = content.encode("utf-8")
        out.write(content)


def mkdir_p(path):
    try:
        os.makedirs(path)
    except OSError as exc:  # Python >2.5
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else:
            raise
