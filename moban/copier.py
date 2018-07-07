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
        for dest_src_pair in file_list:
            for dest, src in dest_src_pair.items():
                self._file_count += 1
                src_path = self._get_src_file(src)
                if src_path is None:
                    reporter.report_error_message(
                        "{0} cannot be found".format(src)
                    )
                elif os.path.isdir(src_path):
                    new_file_pair = []
                    for file_name in os.listdir(src_path):
                        src_file_under_dir = os.path.join(src, file_name)
                        dest_file_under_dir = os.path.join(dest, file_name)
                        new_file_pair.append(
                            {
                                dest_file_under_dir: src_file_under_dir
                            }
                        )
                    self.copy_files(new_file_pair)
                elif HASH_STORE.are_two_file_different(src_path, dest):
                    dest_folder = os.path.dirname(dest)
                    if dest_folder:
                        utils.mkdir_p(dest_folder)
                    reporter.report_copying(src_path, dest)
                    shutil.copy(src_path, dest)
                    self._count = self._count + 1

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
