import os

import fs
import fs.path

from moban.externals import file_system


class BufferedWriter(object):
    def __init__(self):
        self.fs_list = {}

    def write_file_out(self, filename, content):
        if filename == "-":
            print(content.decode())
        elif file_system.is_zip_alike_url(filename):
            self.write_file_out_to_zip(filename, content)
        else:
            write_file_out(filename, content)

    def write_file_out_to_zip(self, filename, content):
        zip_file, file_name = file_system.url_split(filename)
        if zip_file not in self.fs_list:
            self.fs_list[zip_file] = fs.open_fs(zip_file, create=True)
        base_dirs = fs.path.dirname(file_name)
        if not self.fs_list[zip_file].exists(base_dirs):
            self.fs_list[zip_file].makedirs(base_dirs)
        self.fs_list[zip_file].writebytes(file_name, content)

    def close(self):
        for fsx in self.fs_list.values():
            fsx.close()


def write_file_out(filename, content):
    if not file_system.is_zip_alike_url(filename):
        dest_folder = os.path.dirname(filename)
        if dest_folder:
            file_system.mkdir_p(dest_folder)

    file_system.write_bytes(filename, content)
