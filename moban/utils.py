import os
import sys
import yaml
import json
import hashlib

import moban.constants as constants


LABEL_OVERRIDES = 'overrides'
ERROR_DATA_FILE_NOT_FOUND = "Both %s and %s does not exist"
ERROR_DATA_FILE_ABSENT = "File %s does not exist"


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


def search_file(base_dir, file_name):
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


class HashStore:
    IGNORE_CACHE_FILE = False

    def __init__(self):
        self.cache_file = '.moban.hashes'
        if os.path.exists(self.cache_file) and self.IGNORE_CACHE_FILE is False:
            with open(self.cache_file, 'r') as f:
                self.hashes = json.load(f)
        else:
            self.hashes = {}

    def is_file_changed(self, file_name, file_content):
        changed = self._is_source_updated(file_name, file_content)

        if changed is False:
            with open(file_name, 'rb') as target_file:
                target_hash = get_hash(target_file.read())
                if target_hash != self.hashes[file_name]:
                    changed = True
        return changed

    def _is_source_updated(self, file_name, file_content):
        changed = True
        content_hash = get_hash(file_content)
        if os.path.exists(file_name):
            if file_name in self.hashes:
                if content_hash == self.hashes[file_name]:
                    changed = False
        # else the dest file has not been created yet
        # so no need to get content hash at all
        if changed:
            self.hashes[file_name] = content_hash

        return changed

    def close(self):
        with open(self.cache_file, 'w') as f:
            json.dump(self.hashes, f)


def get_hash(content):
    md5 = hashlib.md5()
    md5.update(content)
    return md5.digest().decode('latin1')
