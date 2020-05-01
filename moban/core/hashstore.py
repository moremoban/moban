import json
import hashlib

from moban import constants, exceptions
from moban.externals import file_system


class HashStore:
    IGNORE_CACHE_FILE = False

    def __init__(self):
        self.cache_file = constants.DEFAULT_MOBAN_CACHE_FILE
        if (
            file_system.exists(self.cache_file)
            and self.IGNORE_CACHE_FILE is False
        ):
            with file_system.open_file(self.cache_file) as f:
                self.hashes = json.load(f)
        else:
            self.hashes = {}

    def is_file_changed(self, file_name, file_content, source_template):
        changed, with_permission = self._is_source_updated(
            file_name, file_content, source_template
        )

        if changed is False:
            target_hash = get_file_hash(
                file_name, with_permission=with_permission
            )
            if target_hash != self.hashes[file_name]:
                changed = True
        return changed

    def _is_source_updated(self, file_name, file_content, source_template):
        changed = True
        content = file_content
        with_permission = True
        try:
            content = _mix(
                file_content,
                oct(file_system.file_permissions(source_template)),
            )
        except exceptions.NoPermissionsNeeded:
            # HttpFs does not have getsyspath
            # zip, tar have no permission
            # win32 does not work
            with_permission = False
            pass
        content_hash = get_hash(content)
        if file_system.exists(file_name):
            if file_name in self.hashes:
                if content_hash == self.hashes[file_name]:
                    changed = False
        # else the dest file has not been created yet
        # so no need to get content hash at all
        if changed:
            self.hashes[file_name] = content_hash

        return changed, with_permission

    def save_hashes(self):
        with open(self.cache_file, "w") as f:
            json.dump(self.hashes, f)


HASH_STORE = HashStore()


def get_file_hash(afile, with_permission=True):
    content = file_system.read_bytes(afile)
    try:
        if with_permission:
            content = _mix(content, oct(file_system.file_permissions(afile)))
    except exceptions.NoPermissionsNeeded:
        # HttpFs does not have getsyspath
        # zip, tar have no permission
        # win32 does not work
        pass
    return get_hash(content)


def get_hash(content):
    md5 = hashlib.md5()
    md5.update(content)
    return md5.digest().decode("latin1")


def _mix(content, file_permissions_copy):
    file_permissions_copy = file_permissions_copy.encode("utf-8")
    return content + file_permissions_copy
