import os
import sys
import json
import hashlib

import moban.utils as utils
import moban.constants as constants

PY2 = sys.version_info[0] == 2


class HashStore:
    IGNORE_CACHE_FILE = False

    def __init__(self):
        self.cache_file = constants.DEFAULT_MOBAN_CACHE_FILE
        if os.path.exists(self.cache_file) and self.IGNORE_CACHE_FILE is False:
            with open(self.cache_file, "r") as f:
                self.hashes = json.load(f)
        else:
            self.hashes = {}

    def is_file_changed(self, file_name, file_content, source_template):
        changed = self._is_source_updated(
            file_name, file_content, source_template
        )

        if changed is False:
            target_hash = get_file_hash(file_name)
            if target_hash != self.hashes[file_name]:
                changed = True
        return changed

    def _is_source_updated(self, file_name, file_content, source_template):
        changed = True
        content = _mix(
            file_content, oct(utils.file_permissions(source_template))
        )
        content_hash = get_hash(content)
        if os.path.exists(file_name):
            if file_name in self.hashes:
                if content_hash == self.hashes[file_name]:
                    changed = False
        # else the dest file has not been created yet
        # so no need to get content hash at all
        if changed:
            self.hashes[file_name] = content_hash

        return changed

    def save_hashes(self):
        with open(self.cache_file, "w") as f:
            json.dump(self.hashes, f)


HASH_STORE = HashStore()


def get_file_hash(afile):
    with open(afile, "rb") as handle:
        content = handle.read()
    content = _mix(content, oct(utils.file_permissions(afile)))
    return get_hash(content)


def get_hash(content):
    md5 = hashlib.md5()
    md5.update(content)
    return md5.digest().decode("latin1")


def _mix(content, file_permissions_copy):
    if not PY2:
        file_permissions_copy = file_permissions_copy.encode("utf-8")
    return content + file_permissions_copy
