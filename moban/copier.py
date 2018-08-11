import os
import shutil

import moban.utils as utils
import moban.reporter as reporter
from moban.hashstore import HASH_STORE


class Copier(object):
    def __init__(self, template_dirs):
        self.template_dirs = template_dirs
        self._file_count = 0
        self._count = 0

    def copy_files(self, file_list):
        for dest, src in _iterate_list_of_dicts(file_list):
            src_path = self._get_src_file(src)
            if src_path is None:
                if src.endswith("**"):
                    source_dir = src[:-3]
                    src_path = self._get_src_file(source_dir)
                    if src_path:
                        self._copy_dir_recursively(src[:-3], src_path, dest)
                    else:
                        reporter.report_error_message(
                            "{0} cannot be found".format(source_dir)
                        )
                else:
                    reporter.report_error_message(
                        "{0} cannot be found".format(src)
                    )
            elif os.path.isdir(src_path):
                self._copy_dir(src, src_path, dest)
            elif HASH_STORE.are_two_file_different(src_path, dest):
                self._increment_file_count()
                self._copy(src_path, dest)

    def number_of_copied_files(self):
        return self._count

    def report(self):
        if self._count:
            reporter.report_copying_summary(self._file_count, self._count)
        else:
            reporter.report_no_copying()

    def _get_src_file(self, src):
        for folder in self.template_dirs:
            path = os.path.join(folder, src)
            if os.path.exists(path):
                return path
        else:
            return None

    def _copy_dir(self, source, actual_source_path, dest):
        new_file_pair = []
        for file_name in os.listdir(actual_source_path):
            real_src_file = os.path.join(actual_source_path, file_name)
            if os.path.isfile(real_src_file):
                self._increment_file_count()
                src_file_under_dir = os.path.join(source, file_name)
                dest_file_under_dir = os.path.join(dest, file_name)
                new_file_pair.append({dest_file_under_dir: src_file_under_dir})
        if len(new_file_pair) > 0:
            self.copy_files(new_file_pair)

    def _copy_dir_recursively(self, source, actual_source_path, dest):
        new_file_pair = []
        for file_name in os.listdir(actual_source_path):
            self._increment_file_count()
            src_file_under_dir = os.path.join(source, file_name)
            dest_file_under_dir = os.path.join(dest, file_name)
            real_src_file = os.path.join(actual_source_path, file_name)
            if os.path.isfile(real_src_file):
                new_file_pair.append({dest_file_under_dir: src_file_under_dir})
            elif os.path.isdir(real_src_file):
                new_file_pair.append(
                    {
                        dest_file_under_dir: os.path.join(
                            src_file_under_dir, "**"
                        )
                    }
                )
        self.copy_files(new_file_pair)

    def _copy(self, src_path, dest):
        dest_folder = os.path.dirname(dest)
        if dest_folder:
            utils.mkdir_p(dest_folder)
        reporter.report_copying(src_path, dest)
        shutil.copy(src_path, dest)
        self._count = self._count + 1

    def _increment_file_count(self):
        self._file_count += 1


def _iterate_list_of_dicts(list_of_dict):
    for adict in list_of_dict:
        for key, value in adict.items():
            yield (key, value)
